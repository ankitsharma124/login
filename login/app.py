
import json
import boto3
from datetime import datetime, timedelta
import jwt

JWT_SECRET = 'secret'
JWT_ALGORITHM = 'HS256'
JWT_EXP_DELTA_SECONDS = 20

# import requests

table_name = 'user'
dynamo = boto3.client('dynamodb', region_name='ap-northeast-1')
def respond(err, res=None):
    return {
        'statusCode': 400 if err else 200,
        'body': err.message if err else json.dumps(res),
        'headers': {
            'Content-Type': 'application/json'
        }
    }

def lambda_handler(event, context):
    operations = {
        'DELETE': lambda dynamo, x: dynamo.delete_item(**x),
        'GET': lambda dynamo, x: dynamo.scan(**x),
        'POST': lambda dynamo, x: dynamo.put_item(**x),
        'PUT': lambda dynamo, x: dynamo.update_item(**x)
        }

    operation = event['httpMethod']
    if operation in operations:
        if operation == 'GET':
            payload = {'TableName': 'users'}
            return respond(None, operations[operation](dynamo, payload))
        elif operation == 'POST':
            payload = json.loads(event['body'])
            print(payload)
            req = { 'TableName' : 'users', 'Item' : { 'user_id': {'S': payload['user_id']}, 'first_name': { 'S' :payload['first_name']}, 'last_name': { 'S': payload['last_name']} }}
            #return respond(None, operations[operation](dynamo, req))
            operations[operation](dynamo, req)
            ret = {
                'user_id' : payload['user_id'],
                'exp': datetime.utcnow() + timedelta(seconds=JWT_EXP_DELTA_SECONDS)
            }
            jwt_token = jwt.encode(ret, JWT_SECRET, JWT_ALGORITHM)
            return respond( None, {'token': jwt_token.decode('utf-8')})
    else:
        return respond(ValueError('Unsupported method "{}"'.format(operation)))