# for aws lambda


import shioaji as sj
import json


def lambda_handler(event, context):
    api_key = event["apiKey"]
    secret_key = event["secretKey"]
    if len(api_key) > 0 and len(api_key) > 0:
        api = sj.Shioaji(simulation=True)
        accounts = api.login(api_key, secret_key)
        if len(accounts) > 1:
            return {"statusCode": 200, "body": accounts[0].account_id}
        else:
            return {"statusCode": 404, "body": accounts[0].account_id}
    else:
        return {"statusCode": 400, "body": json.dumps("Bad Request")}
