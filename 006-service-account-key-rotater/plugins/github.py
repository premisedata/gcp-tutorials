from github import Github
from plugins.base import BasePlugin
from core.secrets_manager import SecretManagerClient
from os import environ
from constants import (
    GH_ORG_FIELD,
    GH_REPO_FIELD,
    SECRET_NAME_FIELD,
    TYPE_FIELD,
    DEFAULT_SECRET_NAME,
)


GH_ORGANIZATION = environ.get("GH_ORGANIZATION")
secrets_manager_client = SecretManagerClient()


class GithubPlugin(BasePlugin):
    """Base class for Github API"""

    type = "github"
    count = 0

    schema = {
        GH_ORG_FIELD: "",
        GH_REPO_FIELD: "",
        SECRET_NAME_FIELD: DEFAULT_SECRET_NAME,
    }

    def __init__(self):
        """Constructor for Github Client

        Args:
            token (str): Access Token
            organization (str, optional): Name of Github Organization
        """
        self.client = Github(
            secrets_manager_client.get_latest_secret_version("GH_TOKEN")
        )
        self.organization = GH_ORGANIZATION

    def create_secret_for_repo(self, repo, secret_name, key):
        repo = self.client.get_repo(self.organization + "/" + repo)
        repo.create_secret(secret_name.upper(), key)

    def create_secret_for_organization(self, secret_name, key):
        organization = self.client.get_organization(self.organization)
        organization.create_secret(secret_name.upper(), key, "selected", [])

    def initalize_backend(self, schema, key):
        if self.is_type(schema[TYPE_FIELD]):
            if schema.get(GH_ORG_FIELD, False):
                self.create_secret_for_organization(schema[SECRET_NAME_FIELD], key)
            elif schema[GH_REPO_FIELD]:
                self.create_secret_for_repo(
                    schema[GH_REPO_FIELD], schema[SECRET_NAME_FIELD], key
                )

    def update_key(self, schemas, key):
        for schema in schemas:
            if self.is_type(schema[TYPE_FIELD]):
                if bool(schema.get(GH_ORG_FIELD, False)):
                    self.create_secret_for_organization(schema[SECRET_NAME_FIELD], key)
                elif schema[GH_REPO_FIELD]:
                    self.create_secret_for_repo(
                        schema[GH_REPO_FIELD], schema[SECRET_NAME_FIELD], key
                    )


def initialize():
    return GithubPlugin()
