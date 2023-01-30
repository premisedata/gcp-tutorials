from goblet import Goblet, goblet_entrypoint

app = Goblet(function_name="example-remote-function")
goblet_entrypoint(app)

@app.bqremotefunction(
    dataset_id="example-data-set"
)
def example_function(x: int, y: int) -> int:
    return x*y