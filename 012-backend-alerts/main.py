from goblet import Goblet, goblet_entrypoint, Response
from goblet.infrastructures.alerts import (
    MetricCondition,
    LogMatchCondition,
    CustomMetricCondition,
)
import logging
import time

app = Goblet(function_name="example-cloudfunction-alerts")
goblet_entrypoint(app)

app.log.setLevel(logging.DEBUG)  # configure goblet logger level

# Example Metric Alert for the cloudfunction metric execution_times with a threshold of 1000 ms
app.alert(
    "metric",
    conditions=[
        MetricCondition(
            "test",
            metric="cloudfunctions.googleapis.com/function/execution_times",
            value=1000,
            aggregations=[
                {
                    "alignmentPeriod": "300s",
                    "crossSeriesReducer": "REDUCE_NONE",
                    "perSeriesAligner": "ALIGN_PERCENTILE_50",
                }
            ],
        )
    ],
)

# Example Log Match metric that will trigger an incendent off of any Error logs
app.alert("log-error", conditions=[LogMatchCondition("error", "severity>=ERROR")])

# Example Metric Alert that creates a custom metric for errors and creates an alert with a threshold of 1
app.alert(
    "custom-error",
    conditions=[
        CustomMetricCondition(
            "custom-metric",
            metric_filter="severity=(ERROR OR CRITICAL OR ALERT OR EMERGENCY)",
            value=1,
        )
    ],
)


@app.http()
def main(request):
    # Set a delay
    delay = app.current_request.headers.get("X-DELAY", 0)
    time.sleep(int(delay))

    # Raise error
    error = app.current_request.headers.get("X-ERROR", None)
    if error:
        app.log.error("ERROR")
        return Response("ERROR", status_code=500)

    return "200"
