import json

def lambda_handler(event, context):
    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "Get API for Login"
            # "location": ip.text.replace("\n", "")
        }),
    }