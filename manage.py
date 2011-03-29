from werkzeug import serving
from werkzeug.debug import DebuggedApplication

def make_server():
    from server.application import Server
    return Server()

app = make_server()
app = DebuggedApplication(app, evalex=True)
serving.run_simple('0.0.0.0', 5000, app, use_debugger=True, use_reloader=True)
