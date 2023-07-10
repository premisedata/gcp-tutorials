import logging
from goblet import Goblet, goblet_entrypoint

# goblet setup
app = Goblet(function_name="goblet-iam-tutorial")
goblet_entrypoint(app)

# set debug level
app.log.setLevel(logging.DEBUG)

# Define resources 

# Pubsub Topic
app.pubsub_topic("test")

# Pubsub Subscription
@app.pubsub_subscription(topic="test", use_subscription=True)
def subscription(data):
    return "success"

# Cloud Scheduler
@app.schedule("1 * * * *")
def schedule():
    return "success"