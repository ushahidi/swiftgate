# SwiftGate Controller
# ====================
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
import pika
 
app = Flask(__name__)
 
@app.route('/<api_name>/<path:path>', methods=['GET', 'POST'])
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
    
    log_data = dict(api=api_name, path=path, data=request.data, response=api_response_content)
    log_entry = json.dump(log_data)

    mq_channel.basic_publish(exchange='', routing_key='swiftgate', body=log_entry)

    return gateway_response

def main():
    mq_connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    mq_channel = mq_connection.channel()
    mq_channel.queue_declare(queue='swiftgate')

    app.debug = True
    app.run(host='0.0.0.0')

if __name__ == '__main__':
    main()