import math
import re
from goblet_gcp_client import Client

def convert_units(value, value_field_name):
    number = int(re.findall("\d+", value)[0])
    if value_field_name == "cpu":
        if "m" not in value:
            return number * 1000
        else:
            return number
    elif value_field_name == "memory":
        if "Gi" in value:
            return number * 1024
        else:
            return number

class CloudRun:
    """Cloud Run Usage Alerts"""

    def __init__(self, app, metrics_client, query, min_threshold, min_config, project_id="{project_id}", value_field_name="value"):
        """Constructor for Secret Manager Client"""
        self.services_under_threshold = self.get_services_under_threshold(
            app, metrics_client, query, min_threshold, min_config, project_id, value_field_name)
        

    def get_services_under_threshold(self, app, metrics_client, query, min_threshold, min_config, project_id="{project_id}", value_field_name="value"):
        cloud_run_client = Client(
            "run",
            "v2",
            calls="projects.locations.services",
        )

        # get cpu usage by service
        usage_by_service = metrics_client.execute("query", parent_key="name", parent_schema=f"projects/{project_id}", params={
            "body": {
                "query": query,
            },
        })

        app.log.debug(usage_by_service)
        services = []
        if usage_by_service["timeSeriesDescriptor"]:
            # get unit to get the correct percentage
            point_unit = eval(usage_by_service["timeSeriesDescriptor"]
                              ["pointDescriptors"][0]["unit"].split(".")[0].replace("^", "**"))
            # Build a list of services that are under the threshold
            for service in usage_by_service["timeSeriesData"]:
                service_name = service["labelValues"][0]["stringValue"]
                location = service["labelValues"][1]["stringValue"]

                try:
                    containers = cloud_run_client.execute(
                        "get", parent_key="name", parent_schema=f"projects/{project_id}/locations/{location}/services/{service_name}")["template"]["containers"]
                except Exception as e:
                    app.log.info(
                        f"Skipping service {service_name} because it does not exist")
                    continue
                
                if len(containers) > 1:
                    app.log.info(
                        f"Skipping service {service_name} because it has more than one container")
                    continue

                limit = convert_units(containers[0]['resources']['limits'][value_field_name], value_field_name)
                app.log.debug(f"service {service_name} {value_field_name} limit: {limit} original: {containers[0]['resources']['limits'][value_field_name]}")

                should_alert = (
                    service["pointData"][0]["values"][0]["doubleValue"] * point_unit < min_threshold and
                    limit > min_config
                )

                if should_alert:
                    services.append({
                        "name": service_name,
                        f"{value_field_name}": math.ceil(service["pointData"][0]["values"][0]["doubleValue"] * point_unit),
                    })

        return services
