import os
import json
from goblet import Goblet, goblet_entrypoint
from google.cloud import storage

PROJECT = os.environ["GOOGLE_PROJECT"]
app = Goblet(function_name="bucket-replicator")
goblet_entrypoint(app)

with open("bucket_replications.json") as file:
    bucket_replications = json.load(file)

for src in bucket_replications[PROJECT].keys():
    @app.storage(src, "finalize")
    def replicate(event):
        """Triggered by bucket create/modify blob. Copies the blob to all target buckets

        :param event: bucket create/mobdify blob event
        """
        bucket = event["bucket"]
        name = event["name"]
        if name[-1] == '/':
            app.log.info("Folder creation... skipping")
            return
        storage_client = storage.Client()
        src_bucket = storage_client.bucket(bucket)
        src_blob = src_bucket.blob(name)
        dests = bucket_replications[PROJECT][bucket]
        for dest in dests:
            app.log.info(f"Copying {bucket}/{name} to {dest}")
            dest_bucket = storage_client.bucket(dest)
            src_bucket.copy_blob(src_blob, dest_bucket)

    @app.storage(src, "delete")
    def delete(event):
        """Triggered by bucket delete blob. Deletes the blob in all target buckets

        :param event: bucket create/mobdify blob event
        """
        bucket = event["bucket"]
        name = event["name"]
        if name[-1] == '/':
            app.log.info("Folder creation... skipping")
            return
        storage_client = storage.Client()
        dests = bucket_replications[PROJECT][bucket]
        for dest in dests:
            app.log.info(f"Deleting {dest}/{name}")
            dest_bucket = storage_client.bucket(dest)
            dest_bucket.delete_blob(name)
