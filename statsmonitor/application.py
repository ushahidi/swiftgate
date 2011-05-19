__author__ = "Matthew Kidza-Griffiths"
__copyright__ = "Copyright 2007, Swiftly.org"
__credits__ = ["Matthew Kidza-Griffiths", "Jon Gosier"]
__license__ = "LGPL"
__version__ = "0.0.1"
__maintainer__ = "Matthew Kidza-Griffiths"
__email__ = "mg@swiftly.org"
__status__ = "Development"


from flask import Flask, render_template
from domain.utils import *
from domain.models import *

app = Flask(__name__)

@app.route('/')
def stats():
    wrappers = con.APIWrapper.find()
    statobjects = con.APIUsageStatistics.find()
    stats = {}
    for stat in statobjects:
        wrapper_id = stat.api_wrapper_id
        for wrapper in wrappers:
            if unicode(wrapper._id) == wrapper_id:
                stats[wrapper.display_name] = stat.methods
    return render_template('stats.html', stats=stats)
