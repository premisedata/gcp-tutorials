from googleapiclient import discovery
from oauth2client.client import GoogleCredentials
from datetime import datetime
from os import environ


KEY_VALID_DAYS = int(environ.get("KEY_VALID_DAYS", "2"))


class ServiceAccountsClient:
    """Base Class for Google Cloud Service Account Interactions"""

    def __init__(self):
        """Constructor for Service Account Client"""
        credentials = GoogleCredentials.get_application_default()
        service = discovery.build("iam", "v1", credentials=credentials)
        self.client = service.projects().serviceAccounts()

    def create_key(self, service_account_name):
        """Create Key for Service Account

        Args:
            service_account_name (str): Name of Service Account
        Returns:
            Service Account Key
        """
        key = self.client.keys().create(name=service_account_name).execute()
        return key["privateKeyData"]

    def delete_old_keys(self, service_account_name):
        """Delete old keys associated with Service Account

        Args:
            service_account_name (str): Name of Service Account
        """
        resp = (
            self.client.keys()
            .list(name=service_account_name, keyTypes=["USER_MANAGED"])
            .execute()
        )
        keys = resp.get("keys", [])
        for k in keys:
            if (
                datetime.now().astimezone()
                - datetime.fromisoformat(k["validAfterTime"].replace("Z", "+00:00"))
            ).days > KEY_VALID_DAYS:
                self.client.keys().delete(name=k["name"]).execute()
