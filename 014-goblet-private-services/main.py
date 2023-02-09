import os

import redis
from goblet import Goblet, goblet_entrypoint

app = Goblet(
    function_name="goblet-private-services", backend="cloudrun", routes_type="cloudrun"
)
goblet_entrypoint(app)

app.vpcconnector("goblet-vpcconnector")
app.redis("goblet-redis")

redis_host = os.environ.get("REDIS_HOST", "localhost")
redis_port = int(os.environ.get("REDIS_PORT", 6379))
redis_client = redis.StrictRedis(host=redis_host, port=redis_port)


@app.route("/redis", methods=["GET"])
def index():
    value = redis_client.incr("counter", 1)
    return {"Visitor number": value}
