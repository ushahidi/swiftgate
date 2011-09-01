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

import sys
sys.path.append('/usr/lib/python2.7/site-packages/')

from flask import abort, Flask, make_response, request, abort
from httplib import HTTPConnection
from scribe import scribe
from thrift.transport import TTransport, TSocket
from thrift.protocol import TBinaryProtocol
import json, pika, memcache
 
app = Flask(__name__)

log_entry = scribe.LogEntry('swiftgate', 'Started Up')
socket = TSocket.TSocket(host='localhost', port=1463)
transport = TTransport.TFramedTransport(socket)
protocol = TBinaryProtocol.TBinaryProtocol(trans=transport, strictRead=False, strictWrite=False)
client = scribe.Client(iprot=protocol, oprot=protocol)
transport.open()
result = client.Log(messages=[log_entry])
transport.close()

pika_parameters = pika.ConnectionParameters('localhost')
pika_connection = pika.BlockingConnection(pika_parameters)
pika_channel = pika_connection.channel()
pika_channel.queue_declare(queue='swiftgate', durable=True)

membase = memcache.Client(['127.0.0.1:11211'])

@app.route('/<api_name>/<path:path>', methods=['GET', 'POST'])
def api(api_name, path):
    c = membase.incr(request.environ['REMOTE_ADDR'])
    if c == None:
        membase.set(request.environ['REMOTE_ADDR'], 1, 86400)
    elif c > 50000:
        abort(403)

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
    log_entry = json.dumps(log_data)
    
    pika_channel.basic_publish(exchange='', routing_key='swiftgate', body=log_entry)

    return gateway_response

def main():
    app.debug = True
    app.run(host='0.0.0.0')

if __name__ == '__main__':
    main()
