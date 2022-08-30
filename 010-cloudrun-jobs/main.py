from goblet import Goblet, goblet_entrypoint
import logging 

app = Goblet(function_name="example-job", backend="cloudrun")
goblet_entrypoint(app)
app.log.setLevel(logging.DEBUG)  # configure goblet logger level


@app.job("test")
def job1_task_1(id):
    app.log.info(f"execution test {id}")
    return "200"

@app.job("test", task_id=1)
def job2_task_2(id):
    app.log.info(f"second task {id}")
    return "200"

@app.job("test-schedule", schedule="* * * * *")
def job2(id):
    app.log.info(f"execution every min")
    return "200"