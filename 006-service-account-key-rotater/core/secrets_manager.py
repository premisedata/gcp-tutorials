from google.cloud import secretmanager
from datetime import datetime, timedelta
from os import environ
from google.protobuf.timestamp_pb2 import Timestamp
from google.protobuf.duration_pb2 import Duration

KEY_VALID_DAYS = int(environ.get("KEY_VALID_DAYS", "2"))
ROTATION_PERIOD_SECONDS = environ.get("ROTATION_PERIOD_SECONDS", "86400s")
PROJECT = environ.get("PROJECT")


class SecretManagerClient:
    """Base class for Google Cloud Secret Manager API"""

    def __init__(self):
        """Constructor for Secret Manager Client"""
        self.client = secretmanager.SecretManagerServiceClient()

    def get_latest_secret_version(self, name):
        """Get Latest Version of Secret

        Args:
            name (str): Name of Secret

        Returns:
            Secret Payload
        """
        response = self.client.access_secret_version(
            name=f"projects/{PROJECT}/secrets/{name}/versions/latest"
        )
        return response.payload.data.decode()

    def create_secret(self, service_account_name, project, labels):
        """Creates Secret to be rotated

        Args:
            service_account_name (str): Name of Service Account to create secret for
            project (str): Name of project associated with service account
            labels (dict): Dictionary of labels associated with secret to be created

        Returns:
            Secret Manager Secret
        """
        timestamp = Timestamp()
        duration = Duration()
        timestamp.FromDatetime(
            datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
            + timedelta(1)
        )
        duration.FromJsonString(ROTATION_PERIOD_SECONDS)  # 1 days
        secret = self.client.create_secret(
            request={
                "parent": f"projects/{PROJECT}",
                "secret_id": f"{service_account_name}-{project}",
                "secret": {
                    "replication": {"automatic": {}},
                    "topics": [{"name": f"projects/{PROJECT}/topics/secret-rotation"}],
                    "rotation": {
                        "next_rotation_time": timestamp,
                        "rotation_period": duration,
                    },
                    "labels": {
                        "type": "service_account_key",
                        "service_account_name": service_account_name,
                        "project": project,
                        **labels,
                    },
                },
            }
        )
        return secret

    def create_secret_version(self, secret_name, key):
        """Create Secret Version

        Args:
            name (str): Name of Secret
            key (str): Encoded Service Account Key
        """
        self.client.add_secret_version(
            request={"parent": secret_name, "payload": {"data": key}}
        )

    def delete_old_secret_versions(self, secret_name):
        """Delete Old (Expired) Secret Versions

        Args:
            secret_name (str): Name of Secret
        """
        versions = self.client.list_secret_versions(request={"parent": secret_name})
        old = []
        for v in versions:
            if (
                v.state.name == "ENABLED"
                and (datetime.now().astimezone() - v.create_time).days > KEY_VALID_DAYS
            ):
                old.append(v)
        for old_v in old:
            self.client.destroy_secret_version(name=old_v.name)
