'''
## Special Thanks

reference : https://code.google.com/p/kjk/source/browse/trunk/scripts/test_parse_s3_log.py
reference : http://qiita.com/marcy-terui/items/6dbf2969bc69fd3d6c13
reference : http://qiita.com/ikawaha/items/c654f746cfe76b888a27
'''

from __future__ import print_function
import re
import os
import logging
import sys
import json
import ast
import datetime
from datetime import datetime as dt
import time
import pytz
from elasticsearch import Elasticsearch
import urllib
import boto3
from boto3.session import Session

session = Session(
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
    region_name=os.getenv('AWS_REGION')
)

sqs = session.resource('sqs')
s3 = session.client('s3')
es = Elasticsearch(os.getenv('ES_ENDPOINT'))
es_index = os.getenv('ES_PREFIX') + "-" + dt.now().strftime('%Y-%m-%d')
es_type  = os.getenv('ES_PREFIX')

s3_line_logpats  = r'(\S+) (\S+) \[(.*?)\] (\S+) (\S+) ' \
           r'(\S+) (\S+) (\S+) "([^"]+)" ' \
           r'(\S+) (\S+) (\S+) (\S+) (\S+) (\S+) ' \
           r'"([^"]+)" "([^"]+)"'

s3_line_logpat = re.compile(s3_line_logpats)

s3_names = ("bucket_owner", "bucket", "datetime", "ip", "requestor_id", 
"request_id", "operation", "key", "http_method_uri_proto", "http_status", 
"s3_error", "bytes_sent", "object_size", "total_time", "turn_around_time",
"referer", "user_agent")

logging.basicConfig(stream=sys.stdout, level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

def parse_s3_log_line(line):
    match = s3_line_logpat.match(line.strip())
    result = [match.group(1+n) for n in range(17)]
    return result

def dump_parsed_s3_line(parsed):
    log = {}
    for (name, val) in zip(s3_names, parsed):
        if name == 'datetime':
            val = datetime.datetime.strptime(val.split(' ')[0], '%d/%b/%Y:%H:%M:%S').replace(tzinfo=pytz.utc)
            val = val.isoformat()
        log.update(ast.literal_eval('{"%s": "%s"}' % (name, val)))
    return json.dumps(log)

def post_to_es(line):
    for l in line.split('\n'):
        if re.match('^\s*$', l) == None:
            parsed = parse_s3_log_line(l)
            line = dump_parsed_s3_line(parsed)
            es.index(index=es_index, doc_type=es_type, body=line)

def recive_event_message():
    queue = sqs.get_queue_by_name(QueueName=os.getenv('SQS_QUEUE_NAME'))
    for message in queue.receive_messages(MessageAttributeNames=['*']):
       body = message.body
       message.delete()
       return json.loads(body)

def main():
    while 1:
        logging.info("Start polling...")
        time.sleep(10) 
        event = recive_event_message()
        if event == None:
            logging.info("Event does not exists...")
            continue
        bucket = event['Records'][0]['s3']['bucket']['name']
        key = urllib.unquote_plus(event['Records'][0]['s3']['object']['key']).decode('utf8')
        try:
            logging.info('Getting object {} from bucket {}.'.format(key, bucket))
            response = s3.get_object(Bucket=bucket, Key=key)
            body = response['Body'].read()
            post_to_es(body.decode('utf-8'))
        except Exception as e:
            print(e)
            logging.error('Error getting object {} from bucket {}. Make sure they exist and your bucket is in the same region as this function.'.format(key, bucket))
            raise e

if __name__ == "__main__":
    main()
