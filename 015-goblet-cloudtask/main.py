from goblet import Goblet, goblet_entrypoint

app = Goblet(function_name="cloudtask-example", backend="cloudrun")
goblet_entrypoint(app)

client = app.cloudtaskqueue("my-queue")


@app.route("/enqueue", methods=["GET"])
def enqueue():
    payload = {"message": {"title": "enqueue"}}
    client.enqueue(target="my_target", payload=payload)
    return {}


@app.cloudtasktarget(name="my_target")
def my_target_handler(request):
    app.log.info(request.json)
    return {}
