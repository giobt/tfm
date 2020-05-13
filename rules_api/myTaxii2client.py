from taxii2client.v20 import Server
server = Server('http://hailataxii.com/taxii-discovery-service', user='guest', password='guest')

print(server.title)

# api_root = server.api_roots[0]
# for collection in api_root.collections[]
#     print(collection.title)
#     print(collection.description)
#     # print(collection.can_read)

