# SwiftGate Controller
# =============================
#
# This file is part of SwiftGate.
#
# SwiftGate is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# SwiftGate is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with SwiftGate.  If not, see <http://www.gnu.org/licenses/>.

from flask import abort, Flask, make_response, request
from httplib import HTTPConnection

import oauth2
from functools import wraps
from werkzeug.exceptions import Unauthorized
 
app = Flask(__name__)
 
oauth_server = oauth2.Server(signature_methods={
            # Supported signature methods
            'HMAC-SHA1': oauth2.SignatureMethod_HMAC_SHA1()
        })
 
def validate_two_leg_oauth():
    """
    Verify 2-legged oauth request. Parameters accepted as
    values in "Authorization" header, or as a GET request
    or in a POST body.
    """
    auth_header = {}
    if 'Authorization' in request.headers:
        auth_header = {'Authorization':request.headers['Authorization']}
 
    req = oauth2.Request.from_request(
        request.method,
        request.url,
        headers=auth_header,
        # the immutable type of "request.values" prevents us from sending
        # that directly, so instead we have to turn it into a python
        # dict
        parameters=dict([(k,v) for k,v in request.values.iteritems()]))
 
    try:
        oauth_server.verify_request(req,
            _get_consumer(request.values.get('oauth_consumer_key')),
            None)
        return True
    except oauth2.Error, e:
        raise Unauthorized(e)
    except KeyError, e:
        raise Unauthorized("You failed to supply the "\
                           "necessary parameters (%s) to "\
                           "properly authenticate "%e)
 
class MockConsumer(object):
    key = 'ConsumerKey'
    secret = 'ConsumerSecret'
 
def _get_consumer(key):
    """
    in real life we'd fetch a consumer object,
    using the provided key, that
    has at the bare minimum the attributes
    key and secret.
    """
    return MockConsumer()
 
def oauth_protect(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        validate_two_leg_oauth()
        return f(*args, **kwargs)
    return decorated_function

@app.route('/<api_name>/<path:path>', methods=['GET', 'POST'])
@oauth_protect
def api(api_name, path):
    apis = {'silcc': 'www.opensilcc.com'}
    path = '/' + path

    if '?' in request.url:
        path += '?' + request.url.split('?')[1]

    api = HTTPConnection(apis[api_name], strict=True)
    api.connect()
    api.request(request.method, path, request.data)
    api_response = api.getresponse()
    api_response_content = api_response.read()
    api.close()

    gateway_response = make_response(api_response_content)
    gateway_response.status_code = api_response.status

    for header in ['Cache-Control', 'Content-Type', 'Pragma']:
        gateway_response.headers[header] = api_response.getheader(header)

    return gateway_response

def main():
    app.debug = True
    app.run(host='0.0.0.0')

if __name__ == '__main__':
    main()
