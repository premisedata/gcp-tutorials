from abc import ABCMeta, abstractmethod
from constants import (
    SERVICE_ACCOUNT_NAME_FIELD,
    PROJECT_FIELD,
    LABEL_DELIMITER,
    TYPE_FIELD,
)


class BasePlugin(metaclass=ABCMeta):
    """Abstract Base Class for Plugins"""

    """
        Please refer to constants.py for more information on commmon fields used.
        These keys are used as as shorthand for referencing:

        gho: Github Organization
        ghr: Github Repository
        sn: Secret Name
    """

    count = 0

    @property
    @abstractmethod
    def type(self):
        """Plugin Type"""
        pass

    @property
    @abstractmethod
    def schema(self):
        """Schema for Plugin, used to set labels and default values"""
        pass

    def is_type(self, type):
        return type == self.type

    def reset_count(self):
        self.count = 0

    @abstractmethod
    def initalize_backend(self, data, key):
        pass

    @abstractmethod
    def update_key(self, data, key):
        pass

    def write_label(self, data):
        # Only hyphens (-), underscores (_), lowercase characters, and numbers are allowed. International characters are allowed.
        if not data[TYPE_FIELD] == self.type:
            return None, None
        return self._write_label(data)

    def _write_label(self, data) -> str:
        label = ""
        for key, value in self.schema.items():
            # Add key and value to label if exists or a default exists
            if data.get(key, value):
                label += (
                    key + LABEL_DELIMITER + str(data.get(key, value)) + LABEL_DELIMITER
                )
        label = label[: len(label) - 2]
        label_key = f"{self.type}{self.count}"
        self.count += 1
        return label_key, label

    def extract_labels(self, labels):
        """Reads Labels and creates a list of Schemas

        Args:
            labels (dict): Dictionary of Labels from Secret Manager

        Returns:
            [dict]: List of Schemas for given Plugin type
        """
        schemas = []
        for key, value in labels.items():
            if self.type in key:
                schema = self.parse_label(value)
                schema[SERVICE_ACCOUNT_NAME_FIELD] = labels[SERVICE_ACCOUNT_NAME_FIELD]
                schema[PROJECT_FIELD] = labels[PROJECT_FIELD]
                schema[TYPE_FIELD] = self.type
                schemas.append(schema)
        return schemas

    def parse_label(self, label):
        spl_label = label.split(LABEL_DELIMITER)
        if len(spl_label) % 2 != 0:
            raise ValueError("Label is not valid")
        parsed_label = {}
        for i in range(0, len(spl_label), 2):
            parsed_label[spl_label[i]] = spl_label[i + 1]
        return parsed_label
