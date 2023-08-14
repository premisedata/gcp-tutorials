from goblet import Goblet, goblet_entrypoint

app = Goblet(function_name="goblet")
goblet_entrypoint(app)


@app.bqremotefunction(dataset_id="tutorial", location="US")
def tutorial(value: int, type: str) -> int:
    if type == "double":
        return value * 2
    if type == "square":
        return value**2
    if type == "zero":
        return 0
    else:
        return value
