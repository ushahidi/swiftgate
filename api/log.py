from scribe import scribe
from thrift.transport import TTransport, TSocket
from thrift.protocol import TBinaryProtocol

category='test'
message='hello world'
log_entry = scribe.LogEntry(category, message)
# depending on thrift version
#   log_entry = scribe.LogEntry(dict(category=category, message=message))

socket = TSocket.TSocket(host='localhost', port=1463)
transport = TTransport.TFramedTransport(socket)
protocol = TBinaryProtocol.TBinaryProtocol(trans=transport, strictRead=False, strictWrite=False)
client = scribe.Client(iprot=protocol, oprot=protocol)

transport.open()
result = client.Log(messages=[log_entry])
transport.close()