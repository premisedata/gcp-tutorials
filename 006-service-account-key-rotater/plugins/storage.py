from google.cloud import storage
from plugins.base import BasePlugin
from os import environ
from datetime import datetime
from constants import (
    SERVICE_ACCOUNT_NAME_FIELD,
    PROJECT_FIELD,
    SECRET_NAME_FIELD,
    DEFAULT_SECRET_NAME,
    TYPE_FIELD,
)

STORAGE_BUCKET_NAME = environ.get("STORAGE_BUCKET_NAME")

class StoragePlugin(BasePlugin):
    """Base class for Google Cloud Storage API"""

    type = "storage"
    count = 0
    schema = {SECRET_NAME_FIELD: DEFAULT_SECRET_NAME}

    def __init__(self):
        """Constructor for Storage Client"""
        self.bucket = storage.Client().get_bucket(STORAGE_BUCKET_NAME)

    def update_secret_in_bucket(self, schema, key):
        """Updates Secret in Bucket

        Args:
            schema (dict): Schema for Storage Object
            key (str): Service Account Key
        """
        service_account_name = schema[SERVICE_ACCOUNT_NAME_FIELD]
        project = schema[PROJECT_FIELD]
        secret_name = schema[SECRET_NAME_FIELD]
        date = datetime.now().strftime("%m%d%Y")
        key_blob = self.bucket.blob(
            f"{service_account_name}-{project}/{secret_name.upper()}_{date}"
        )
        key_blob.upload_from_string(key)

    def initalize_backend(self, schema, key):
        if self.is_type(schema[TYPE_FIELD]):
            self.update_secret_in_bucket(schema, key)

    def update_key(self, schemas, key):
        for schema in schemas:
            if self.is_type(schema[TYPE_FIELD]):
                self.update_secret_in_bucket(schema, key)


def initialize():
    return StoragePlugin()
