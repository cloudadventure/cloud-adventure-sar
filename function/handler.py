import json
import base64
import os

import boto3
with open('h', 'r') as h, open('e', 'r') as e, open('g', 'r') as g, open('t', 'r') as t:
  hdata = base64.b64decode(h.read()).decode('ascii')
  edata = base64.b64decode(e.read()).decode('ascii')
  gdata = base64.b64decode(g.read()).decode('ascii')
  tdata = base64.b64decode(t.read()).decode('ascii')


def lambda_handler(event, context):

    if 'path' not in event:
        raise Exception(edata)
        return 
    elif 'path' in event and event['path'] == '/help' and event['httpMethod'] == 'GET':
        return {
            "statusCode": 200,
            "body": json.dumps({
                "message": hdata
            }),
        }
    elif 'path' in event and event['path'] == '/gong' and event['httpMethod'] == 'POST':
        message = tdata
        kms_client = boto3.client("kms")
        response = kms_client.encrypt(
            KeyId=os.environ["KMS_KEY_ID"],
            Plaintext=tdata
        )
        client = boto3.client('sns')
        response = client.publish(
            TargetArn=os.environ["SNS_ARN"],
            Message=json.dumps({'decrypt_this': response['CiphertextBlob'].decode("ISO-8859-1")})
        )
        return {
            "statusCode": 200,
            "body": json.dumps({
                "message": gdata
            }),
        }
    else:
        return {
            "statusCode": 400,
            "body": json.dumps({
                "message": "Check the instructions and try again ... you are on the wrong track."
            }),
        }
