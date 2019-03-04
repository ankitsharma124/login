import json
import pyjwt
import boto3

#encoded = pyjwt.encode({'some': 'payload'}, 'secret', algorithm='HS512')

def lambda_handler(event, context):
    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": pyjwt.encode({'some': 'payload'}, 'secret', algorithm='HS512')
            # "location": ip.text.replace("\n", "")
        }),
    }