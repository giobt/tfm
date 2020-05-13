import sys
import json

sys.path.append('/home/giorgio/Documents/umu/tfm/source/rules_api/api/compiled_grammar/pattern_grammar')

from antlr4 import *
from flask import Flask
from flask import jsonify
from flask import request
from json import dumps
from kafka import KafkaProducer
from stix2 import Indicator, parse
from stix2.v21 import Location
from stix2validator import validate_instance, print_results
from STIXPatternParser import STIXPatternParser
from STIXPatternLexer import STIXPatternLexer
from STIXPatternVisitor import STIXPatternVisitor
from stix_shifter.stix_translation import stix_translation
from time import sleep
from werkzeug.http import HTTP_STATUS_CODES

class STIXPatternPrintVisitor(STIXPatternVisitor):
  def visitObjectPath(self, ctx):
    type_token = ctx.IdentifierWithoutHyphen() or ctx.IdentifierWithHyphen()
    print(type_token)
    return self.visitChildren(ctx)

  def visitObjectType(self, ctx):
    type_token = ctx.IdentifierWithoutHyphen() or ctx.IdentifierWithHyphen()
    print(type_token)
    return self.visitChildren(ctx)

def handlePattern(pattern):
  # print(pattern)
  for child in pattern.getChildren():
    print(child.getText())


def parse_pattern(data):
  # input_stream = FileStream("../rule_model.json")
  input_stream = InputStream(data)
  lexer = STIXPatternLexer(input_stream)
  stream = CommonTokenStream(lexer)
  parser = STIXPatternParser(stream)
  tree = parser.pattern()
  # handlePattern(tree)

  printer = STIXPatternPrintVisitor()
  res = printer.visit(tree)
    # print(res)

# Get json input
with open('../rule_model.json') as f:
  data = json.load(f)

# Validate input
results = validate_instance(data)
# print_results(results)

# Parse json input to cyber observable object
cbos = parse(data, allow_custom=False, version="21")
# print(type(cbos))
# print(cbos)

# Instantiate STIX Shifter object for parsing indicator patterns into json
translation = stix_translation.StixTranslation()
response = translation.translate('qradar', 'query', '', "[ipv4-addr:value = '127.0.0.1']", '')
print(response)

# Parse indicators only
# for cbo in cbos.objects:
#     if cbo.type == "indicator":
        # Parse pattern
        # response = translation.translate('elastic', 'parse', '\{\}', cbo.pattern, '\{\}')
        # print(response)
        # parse_pattern(cbo.pattern)
        
##########################################################################################
# app = Flask(__name__)

# @app.route("/")
# def hello():
#     return "Hello World!"

# @app.route("/rule/create", methods=['POST'])
# def create():
#     data = request.get_json() or {}
    
#     Validate input
#     if 'Rule' not in data:
#         return bad_request('must include Rule field')

#     # Parse input into suricata rule format
#     rule = parse_rule(data['Rule'])

#     # Initialize kafka broker
#     producer = KafkaProducer(bootstrap_servers=['localhost:9092'],
#                             value_serializer=lambda x: dumps(x).encode('utf-8'))

#     # Send rule to broker
#     producer.send('numtest', value=rule)

#     Return status code
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