from cabby import create_client

client = create_client(
    'test.taxiistand.com',
    use_https=True,
    discovery_path='/read-write/services/discovery')

for service in services:
    print('Service type={s.type}, address={s.address}'
          .format(s=service))

content_blocks = client.poll(collection_name='all-data')

for block in content_blocks:
    print(block.content)

collections = client.get_collections(
    uri='https://test.taxiistand.com/read-write/services/collection-management')