from goblet import Goblet, Response, goblet_entrypoint
import os
import json
from google.api_core.exceptions import AlreadyExists
from core.secrets_manager import SecretManagerClient
from core.service_account import ServiceAccountsClient
from pkg_resources import iter_entry_points
from constants import (
    SERVICE_ACCOUNT_NAME_FIELD,
    PROJECT_FIELD,
    SECRET_NAME_FIELD,
    DEFAULT_SECRET_NAME,
    LABEL_DELIMITER,
)
import logging

app = Goblet(function_name="service-account-key-rotater", local="local")
app.log.setLevel(logging.INFO)
goblet_entrypoint(app)

PROJECT = os.environ.get("PROJECT")

secret_manager_client = SecretManagerClient()
service_account_client = ServiceAccountsClient()

plugins = [
    entry_point.load()()
    for entry_point in iter_entry_points(group="plugins", name=None)
]

LABEL_CHARACTER_LIMIT = 63


@app.topic("secret-rotation", attributes={"eventType": "SECRET_ROTATE"})
def rotate_keys(data):
    secret = json.loads(data)
    sec_project = secret["labels"][PROJECT_FIELD]
    service_account_name = secret["labels"][SERVICE_ACCOUNT_NAME_FIELD]
    # generate new key
    service_account = f"{service_account_name}@{sec_project}.iam.gserviceaccount.com"
    sa_name = f"projects/{sec_project}/serviceAccounts/{service_account}"
    private_key = service_account_client.create_key(sa_name)
    encoded_private_key = private_key.encode()

    # upload new key to secret manager
    secret_manager_client.create_secret_version(secret["name"], encoded_private_key)

    for plugin in plugins:
        schemas = plugin.extract_labels(secret["labels"])
        plugin.update_key(schemas, private_key)

    # destroy old secret version
    secret_manager_client.delete_old_secret_versions(secret["name"])

    # delete old keys
    service_account_client.delete_old_keys(sa_name)

    return "Success"


@app.http()
def create_secret(request):
    data = request.json
    if (
        not data
        or not data.get(SERVICE_ACCOUNT_NAME_FIELD)
        or not data.get(PROJECT_FIELD)
    ):
        return Response("Missing service_account_name or project", status_code=400)

    service_account_name = data[SERVICE_ACCOUNT_NAME_FIELD]
    project = data[PROJECT_FIELD]

    service_account = f"{service_account_name}@{project}.iam.gserviceaccount.com"
    sa_name = f"projects/{project}/serviceAccounts/{service_account}"

    plugin_data = data.get("plugin_data", [])

    for plugin in plugins:
        plugin.reset_count()

    labels = {}
    for info in plugin_data:
        info[SERVICE_ACCOUNT_NAME_FIELD] = data[SERVICE_ACCOUNT_NAME_FIELD]
        info[PROJECT_FIELD] = data[PROJECT_FIELD]
        info[SECRET_NAME_FIELD] = info.get(SECRET_NAME_FIELD, DEFAULT_SECRET_NAME)
        for plugin in plugins:
            label_key, label = plugin.write_label(info)
            if label_key and label:
                labels[label_key] = label.lower()

    for _, value in labels.items():
        if len(value) > LABEL_CHARACTER_LIMIT:
            values = value.split(LABEL_DELIMITER)
            sni = values.index(SECRET_NAME_FIELD)
            return Response(
                f"Failed to create label for Secret, please reduce secret {values[sni + 1]} to {len(values[sni + 1]) - (len(value) - LABEL_CHARACTER_LIMIT)} characters",
                status_code=400,
            )
    try:
        # create new secret
        secret = secret_manager_client.create_secret(
            service_account_name, project, labels
        )
    except AlreadyExists as e:
        return Response(e.message, status_code=409)

    # generate new key
    private_key = service_account_client.create_key(sa_name)
    encoded_private_key = private_key.encode()

    # upload new key to secret manager
    secret_manager_client.create_secret_version(secret.name, encoded_private_key)

    for info in plugin_data:
        for plugin in plugins:
            plugin.initalize_backend(info, private_key)
    return f"Secret Created with name {service_account_name}"
