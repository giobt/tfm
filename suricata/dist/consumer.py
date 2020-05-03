from kafka import KafkaConsumer
from json import loads
import os

consumer = KafkaConsumer(
    os.environ.get('KAFKA_TOPIC'),
     bootstrap_servers=[os.environ.get('KAFKA_BROKER')],
     auto_offset_reset='earliest',
     enable_auto_commit=True,
     group_id=os.environ.get('KAFKA_GROUP_ID'),
     value_deserializer=lambda x: loads(x.decode('utf-8')))

for message in consumer:
    message = message.value

    # Append new rule to local.rules file
    with open("/etc/suricata/rules/local.rules", "a") as file_object:
        file_object.write("{rule}\n".format(rule=message))

    # Update suricata ruleset
    os.system('suricata-update --no-merge')

    # Tell Suricata to do a nonblocking ruleset-reload
    os.system('suricatasc -c ruleset-reload-nonblocking')