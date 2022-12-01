from jina import Client, Document

c = Client(host='grpc://10.4.96.38:51258')
result = c.post('/', Document())

print(result.texts)