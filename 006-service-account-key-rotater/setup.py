from setuptools import setup

setup(
    name="service-account-key-rotater",
    entry_points={
        "plugins": [
            "github=plugins.github:initialize",
            "storage=plugins.storage:initialize",
        ]
    },
)
