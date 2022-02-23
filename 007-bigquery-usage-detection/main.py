from goblet import Goblet, goblet_entrypoint
from google.cloud import bigquery, storage
from slack_sdk.webhook import WebhookClient
from texttable import Texttable
from datetime import datetime, timezone, timedelta
import csv
import os

app = Goblet(function_name="bq-usage-detection", local="local")
goblet_entrypoint(app)

BUCKET = os.environ.get("BUCKET")
PROJECT = os.environ.get("PROJECT")
SLACK_WEBHOOK = os.environ.get("SLACK_WEBHOOK")
UPLOAD_PATH = os.environ.get("UPLOAD_PATH")

webhook = WebhookClient(SLACK_WEBHOOK)
storage_client = storage.Client()


@app.schedule("45 23 * * *", timezone="UTC")
def main():
    jobs, jobs_usage = retrieve_jobs()
    above_avg = [
        job
        for job in jobs[: int(len(jobs) / 2)]
        if job[2] > jobs_usage.get("mean_gigabytes")
    ]

    for job in above_avg:
        job[2] = f"{job[2]:.2f}"

    now = datetime.now(timezone.utc)

    with open("/tmp/high_usage_jobs.csv", "w") as f:
        write = csv.writer(f)
        write.writerow(
            [
                "Job ID",
                "User Email",
                "Gigabytes Processed",
                "Total Slot Usage",
                "Query",
            ]
        )
        write.writerows(above_avg)

    upload_to_gcs(
        BUCKET,
        f"{UPLOAD_PATH}_{now.strftime('%Y-%m-%d')}.csv",
        "/tmp/high_usage_jobs.csv",
    )
    msg = generate_message(above_avg, jobs_usage, now)
    webhook.send(text="daily-bq-usage-alerts", blocks=msg)


def retrieve_jobs():
    """
    retrieve_jobs retrieves the metadata for all BigQuery jobs that have finished running today
    and returns info about these jobs, and info about the mean and median data processed amounts
    (in GB) across all of these jobs

    :return: sorted_jobs, jobs_usage
    """
    client = bigquery.Client(project=PROJECT)
    QUERY = (
        'SELECT job_id, user_email, total_bytes_processed, total_slot_ms, query FROM `region-us`.INFORMATION_SCHEMA.JOBS_BY_PROJECT '
        'WHERE EXTRACT(DATE FROM end_time) = current_date() AND state = "DONE" '
    )

    query_job = client.query(QUERY)
    rows = query_job.result()

    all_jobs = []
    total_gb_processed = 0
    total_jobs_processed = 0

    for row in rows:
        try:
            row_data = list(row)
            gb_processed = 0

            if row_data[2]:
                gb_processed = row_data[2] = row_data[2] / (1024 ** 3)

            if row_data[3]:
                slot_time = str(timedelta(milliseconds=row_data[3])).split(":")
                row_data[
                    3
                ] = f"{slot_time[0]} hr, {slot_time[1]} min, {float(slot_time[2]):.2f} sec"

            if row_data[4]:
                row_data[4] = (
                    (row_data[4][:512] + "...")
                    if len(row_data[4]) > 512
                    else row_data[4]
                )

            if gb_processed > 0:
                all_jobs.append(row_data)
                total_gb_processed += gb_processed
                total_jobs_processed += 1

        except Exception as e:
            print(f"Error: {e}")
            print(
                f"job_id: {row_data[0]} | user_email: {row_data[1]} | total data processed (GB): {row_data[2]} | total_slot_ms: {row_data[3]} | beginning of query: {row_data[4][:100]}"
            )

    sorted_jobs = sorted(all_jobs, key=lambda x: x[2], reverse=True)
    jobs_usage = {
        "mean_gigabytes": total_gb_processed / total_jobs_processed,
        "median_gigabytes": sorted_jobs[int(len(sorted_jobs) / 2)][2],
    }
    return sorted_jobs, jobs_usage


def upload_to_gcs(bucket_name, file_name, data):
    """
    upload_to_gcs publishes a file to the Google Cloud Storage bucket

    :param bucket_name: bucket we are publishing to
    :param file_name: the file path and name we are publishing this file as
    :param data: data to be published to the file
    """
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(file_name)
    blob.upload_from_filename(data, content_type="text/csv")


def generate_message(jobs, jobs_usage, now):
    """
    generate_message formats a Slack message containing info about the
    top 10 high-usage BQ jobs that have finished in the current day

    :param jobs: list of above-average usage BQ jobs and relevant info
    :param jobs_usage: dict containing median and mean data processed amounts for all BQ jobs
    :param now: datetime object containing the current date and time
    :return: message
    """
    message = [
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f"*Most expensive BigQuery jobs today ({now.strftime('%Y-%m-%d')})* (based on total_bytes_processed)",
            },
        }
    ]

    jobs_description = [["job_id", "user_email", "data processed"]]

    for job in jobs[:10]:
        job[0] = (job[0][:21] + "...") if len(job[0]) > 24 else job[0]
        job[4] = (job[4][:125] + "...") if len(job[4]) > 128 else job[4]
        jobs_description.append([job[0], job[1], f"{job[2]} GB"])

    table = Texttable()
    table.add_rows(jobs_description)

    message.extend(
        [
            {
                "type": "section",
                "text": {"type": "mrkdwn", "text": f"```{table.draw()}```"},
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"Our median BQ job processes only *{float(jobs_usage.get('median_gigabytes')):.2f} GB*, and the average data processed across all of our jobs is *{float(jobs_usage.get('mean_gigabytes')):.2f} GB*.\n\nPlease investigate and remediate these high-usage jobs",
                },
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"<https://storage.cloud.google.com/{PROJECT}/{UPLOAD_PATH}_{now.strftime('%Y-%m-%d')}.csv|View all high-usage jobs and their corresponding queries>",
                },
            },
            {"type": "divider"},
        ]
    )
    return message
