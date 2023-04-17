import os
import logging
from goblet import Goblet, jsonify, goblet_entrypoint
from goblet_gcp_client import Client
from utils.cloudrun import CloudRun
from utils.slack_message import send_slack_message
from utils.utility_functions import merge_lists

# goblet setup
app = Goblet(function_name="goblet-gcp-metrics-slack-alerts")
goblet_entrypoint(app)

# set debug level
app.log.setLevel(logging.DEBUG if os.environ.get("DEBUG", "false") == "true" else logging.INFO)

# gcp client
metrics_client = Client(
    "monitoring",
    "v3",
    calls="projects.timeSeries",
    parent_schema="projects/{project_id}"
)
resource_manager_client = Client(
    "cloudresourcemanager",
    "v1",
    calls="projects",
)

# scheduled job
@app.schedule(os.environ.get("CRON_EXPRESSION", "0 15 * * 5"))
def scheduled_job():
    # Get active project ids
    active_projects = resource_manager_client.execute("list")["projects"]
    active_projects = filter(
        lambda project: project["lifecycleState"] == "ACTIVE", active_projects)
    active_projects = filter(
        lambda project: "sys" not in project["projectId"], active_projects)
    active_projects = list(
        map(lambda project: project["projectId"], active_projects))

    for project_id in active_projects:
        app.log.info(f"Checking project: {project_id}")
        services_under_cpu_threshold = []
        services_under_memory_threshold = []

        # Get services under cpu threshold
        services_under_cpu_threshold = CloudRun(
            app=app,
            metrics_client=metrics_client,
            query="""
            fetch cloud_run_revision
            | metric 'run.googleapis.com/container/cpu/utilizations'
            | group_by 1w,
                [value_utilizations_percentile: percentile(value.utilizations, 99)]
            | every 1w
            | group_by [resource.service_name, resource.location],
                [value_utilizations_percentile_max: max(value_utilizations_percentile)]
            """,
            min_threshold=float(os.environ.get(
                "CLOUDRUN_CPU_MIN_THRESHOLD", "10%").replace("%", "")),
            min_config=int(os.environ.get("CLOUDRUN_CPU_MIN_VALUE", "1000")),
            project_id=project_id,
            value_field_name="cpu",
        ).services_under_threshold

        # Get services under memory threshold
        services_under_memory_threshold = CloudRun(
            app=app,
            metrics_client=metrics_client,
            query="""
            fetch cloud_run_revision
            | metric 'run.googleapis.com/container/memory/utilizations'
            | group_by 1w,
                [value_utilizations_percentile: percentile(value.utilizations, 99)]
            | every 1w
            | group_by [resource.service_name, resource.location],
                [value_utilizations_percentile_max: max(value_utilizations_percentile)]
            """,
            min_threshold=float(os.environ.get(
                "CLOUDRUN_MEMORY_MIN_THRESHOLD", "10%").replace("%", "")),
            min_config=int(os.environ.get("CLOUDRUN_MEMORY_MIN_VALUE", "512")),
            project_id=project_id,
            value_field_name="memory",
        ).services_under_threshold

        services = merge_lists(services_under_cpu_threshold, services_under_memory_threshold)
        if services:
            send_slack_message(app, project_id, services)
    return jsonify("success")
