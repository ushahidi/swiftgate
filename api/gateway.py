# SwiftRiver Gateway Controller
# =============================
#
# This file is part of SwiftRiver Gateway.
#
# SwiftRiver Gateway is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# SwiftRiver Gateway is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with SwiftRiver Gateway.  If not, see <http://www.gnu.org/licenses/>.

from flask import abort, Flask, make_response, request
from httplib import HTTPConnection

app = Flask(__name__)

@app.route('/api/<method_name>', methods=['GET', 'POST'])
def api(method_name):
    path = '/api'
    
    if '?' in request.url:
        path += '?' + request.url.split('?')[1]

    api = HTTPConnection('silcc.nrny.net', strict=True)
    api.connect()
    api.request(request.method, path, request.data, request.headers)
    api_response = connection.getresponse()
    api.close()

    gateway_response = make_response(api_response.read())
    gateway_response.status_code = api_response.status

    for header in api_response.getheaders():
        gateway_response.headers[header[0]] = header[1]

    return response

def main():
    app.debug = True
    app.run(host='0.0.0.0')

if __name__ == '__main__':
    main()
