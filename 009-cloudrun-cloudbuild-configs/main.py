from goblet import Goblet, goblet_entrypoint

app = Goblet(function_name = "cloudrun-cloudbuild-configs", backend="cloudrun", routes_type="cloudrun")
goblet_entrypoint(app)

@app.route('/home')
def home():
    return {"hello": "world"}