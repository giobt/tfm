# pip install kafka-python
# docker-compose up -d zookeeper broker
# docker-compose exec broker kafka-topics --create --bootstrap-server localhost:9092 --replication-factor 1 --partitions 1 --topic ids_rules

from kafka import KafkaConsumer
from json import loads
import os

consumer = KafkaConsumer(
    'numtest',
     bootstrap_servers=['localhost:9092'],
     auto_offset_reset='earliest',
     enable_auto_commit=True,
     group_id='my-group',
     value_deserializer=lambda x: loads(x.decode('utf-8')))

for message in consumer:
    message = message.value
    print(message)

    # Append new rule to local.rules file
    # with open("/etc/suricata/rules/local.rules", "a") as file_object:
    #     file_object.write("{rule}\n".format(rule=message))

    # # Update suricata ruleset
    # os.system('suricata-update --no-merge')

    # #Tell Suricata to do a nonblocking ruleset-reload
    # os.system('suricatasc -c ruleset-reload-nonblocking')