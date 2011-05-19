__author__ = "Matthew Kidza-Griffiths"
__copyright__ = "Copyright 2007, Swiftly.org"
__credits__ = ["Matthew Kidza-Griffiths", "Jon Gosier"]
__license__ = "LGPL"
__version__ = "0.0.1"
__maintainer__ = "Matthew Kidza-Griffiths"
__email__ = "mg@swiftly.org"
__status__ = "Development"


from werkzeug import serving
from werkzeug.debug import DebuggedApplication

# Make and run the server
def make_server():
    from server.application import Server
    return Server()


if __name__ == '__main__':
    server = make_server()
    server = DebuggedApplication(server, evalex=True)
    serving.run_simple('0.0.0.0', 5000, server, use_debugger=True, use_reloader=True)


