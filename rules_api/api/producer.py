import sys
import json
import os

sys.path.append('/home/giorgio/Documents/umu/tfm/source/rules_api/api/compiled_grammar/pattern_grammar')

from antlr4 import *
from flask import Flask
from flask import jsonify
from flask import request
from json import dumps
from kafka import KafkaProducer
from stix2 import Indicator, parse
# from stix2.v21 import Location
from stix2validator import validate_instance, print_results
# from STIXPatternParser import STIXPatternParser
# from STIXPatternLexer import STIXPatternLexer
# from STIXPatternVisitor import STIXPatternVisitor
# from stix_shifter.stix_translation import stix_translation
from time import sleep
from werkzeug.http import HTTP_STATUS_CODES

# class STIXPatternPrintVisitor(STIXPatternVisitor):
#   def visitObjectPath(self, ctx):
#     type_token = ctx.IdentifierWithoutHyphen() or ctx.IdentifierWithHyphen()
#     print(type_token)
#     return self.visitChildren(ctx)

#   def visitObjectType(self, ctx):
#     type_token = ctx.IdentifierWithoutHyphen() or ctx.IdentifierWithHyphen()
#     print(type_token)
#     return self.visitChildren(ctx)

# def handlePattern(pattern):
#   # print(pattern)
#   for child in pattern.getChildren():
#     print(child.getText())


# def parse_pattern(data):
#   # input_stream = FileStream("../rule_model.json")
#   input_stream = InputStream(data)
#   lexer = STIXPatternLexer(input_stream)
#   stream = CommonTokenStream(lexer)
#   parser = STIXPatternParser(stream)
#   tree = parser.pattern()
#   # handlePattern(tree)

#   printer = STIXPatternPrintVisitor()
#   res = printer.visit(tree)
#     # print(res)

# Get json input
with open('../imddos.json') as f:
  data = json.load(f)

# Validate input
results = validate_instance(data)
print(results.is_valid)

if results.is_valid:
  print("valid")
else:
  print(results.errors[0].message)
  # for error in results.errors:
  #   print(error.message)

# Parse json input to cyber observable object
# cbos = parse(data, allow_custom=False, version="21")
# print(type(cbos))
# print(cbos)

# Instantiate STIX Shifter object for parsing indicator patterns into json
# translation = stix_translation.StixTranslation()
# response = translation.translate('qradar', 'query', '', "[ipv4-addr:value = '127.0.0.1']", '')
# print(response)

# Parse indicators only
# for cbo in cbos.objects:
#     if cbo.type == "indicator":
#         # Parse pattern
#         # response = translation.translate('elastic', 'parse', '\{\}', cbo.pattern, '\{\}')
#         # parse_pattern(cbo.pattern)
#         # print(cbo.pattern)
#         # response = os.system("stix-shifter translate elastic_ecs parse  \{\} \"[network-traffic:src_ref.type = 'ipv4-addr']\" \{\}")
#         response = os.system("stix-shifter translate elastic_ecs parse  \{\} \"%s\" \{\}" % (cbo.pattern))
        # print(response)
        
##########################################################################################
# app = Flask(__name__)

# kafka_broker = os.environ.get('KAFKA_BROKER') or 'localhost:9092'
# kafka_topic = os.environ.get('KAFKA_TOPIC') or 'numtest'

# @app.route("/health")
# def health():
#     return True

# @app.route("/rule/create", methods=['POST'])
# def create():
#     # Get STIX 2.1 bundle in json format
#     data = request.get_json() or {}
    
#     # Validate input
#     validation = results = validate_instance(data)

#     # Return errors if not valid STIX 2.1 format
#     if not validation.is_valid:
#         return bad_request(validation.errors[0].message)
    
#     # Initialize kafka broker
#     producer = KafkaProducer(bootstrap_servers=[kafka_broker],
#                             value_serializer=lambda x: dumps(x).encode('utf-8'))

#     # Send content to broker
#     producer.send(kafka_topic, value=data)

#     # Return status code
#     return "response"

# def error_response(status_code, message=None):
#     payload = {'error': HTTP_STATUS_CODES.get(status_code, 'Unknown error')}
#     if message:
#         payload['message'] = message
#     response = jsonify(payload)
#     response.status_code = status_code
#     return response

# def bad_request(message):
#     return error_response(400, message)

# if __name__ == '__main__':
#     app.run(debug=True)