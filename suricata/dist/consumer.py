# pip install kafka-python
# docker-compose up -d zookeeper broker
# docker-compose exec broker kafka-topics --create --bootstrap-server localhost:9092 --replication-factor 1 --partitions 1 --topic ids_rules

from kafka import KafkaConsumer
from json import loads
from stix2 import Indicator, parse
from stix_shifter.stix_translation import stix_translation

import os
import json
import random

kafka_broker = os.environ.get('KAFKA_BROKER') or 'localhost:9092'
kafka_topic = os.environ.get('KAFKA_TOPIC') or 'numtest'
kafka_group_id = os.environ.get('KAFKA_GROUP_ID') or 'my-group'

action = 'alert'

# Generate rule SID (1000000-1999999 Reserved for Local Use)
sid = 1000000 

consumer = KafkaConsumer(
    kafka_topic,
     bootstrap_servers=[kafka_broker],
     auto_offset_reset='earliest',
     enable_auto_commit=True,
     group_id=kafka_group_id,
     value_deserializer=lambda x: loads(x.decode('utf-8')))

def parse_stix2suricata(options, 
                        action='alert', protocol='tcp',
                        src_ip='$HOME_NET', src_port='any', direction='->', dst_ip='$EXTERNAL_NET', dst_port='any'):

    return f"{action} {protocol} {src_ip} {src_port} {direction} {dst_ip} {dst_port} ({''.join(options)})"

def parse_observations(cbo):
    rules = []
    sid  = sid + 1

    # Initialize rule options list with message
    options = [ f"message: \"{cbo.name.upper()} {cbo.description}\"; sid: {sid}" ]

    # Generate json object from pattern
    translation = stix_translation.StixTranslation()
    observationExpressions = translation.translate(module = 'elastic_ecs', # Provides more useful structure
                                    translate_type = 'parse',
                                    data_source = None,
                                    data = cbo.pattern)

    for observationExpression in observationExpressions['parsed_stix']:
        attribute = observationExpression['attribute'].split(':')
        if attribute[0] == 'url':
            # Parse URL Object {type: 'string' must be 'url', value: 'string' MUST conform to [RFC3986]}
            content = f"content: \"{observationExpression['value']}\"; "
            options.append(content)

            # Generate Suricata rule
            rule = parse_stix2suricata(options=options)

            # Add rule to response list
            rules.append(rule)
    return rules

# For each message in kafka
for message in consumer:
    # Start measuring execution time
    start_time = time.time()

    # Parse message to STIX 2.1 bundle
    bundle = parse(message.value, allow_custom=False, version="21")
    # bundle = parse(message, allow_custom=False, version="21")

    # For each cyber observable in the bundle
    rules = []
    for cbo in bundle.objects:
        # Verify object is a STIX Indicator
        if cbo.type == "indicator":
  
            # Parse input into suricata rule format
            rules = rules + parse_observations(cbo)
    
    # Append new rule to local.rules file
    with open("/etc/suricata/rules/local.rules", "a") as file_object:
        file_object.write("{rules}\n".format(rules='\n'.join(rules)))

    # Update suricata ruleset
    os.system('suricata-update --no-merge')

    #Tell Suricata to do a nonblocking ruleset-reload
    os.system('suricatasc -c ruleset-reload-nonblocking')

    # Finish measuring execution time
    end_time = time.time()
    ellapsed_time = end_time - start_time

    # Return status code
    print("--- %s seconds ---" % (ellapsed_time))

