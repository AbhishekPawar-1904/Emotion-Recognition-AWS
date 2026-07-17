"""
Returns stored emotion-detection results for a given image key.
"""

import json
import os
from decimal import Decimal

import boto3

dynamodb = boto3.resource('dynamodb')
RESULTS_TABLE = os.environ['RESULTS_TABLE']
table = dynamodb.Table(RESULTS_TABLE)

CORS_HEADERS = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Allow-Methods': 'OPTIONS,GET'
}


def decimal_to_native(obj):
    if isinstance(obj, list):
        return [decimal_to_native(v) for v in obj]
    if isinstance(obj, dict):
        return {k: decimal_to_native(v) for k, v in obj.items()}
    if isinstance(obj, Decimal):
        return float(obj) if obj % 1 else int(obj)
    return obj


def lambda_handler(event, context):
    params = event.get('queryStringParameters') or {}
    key = params.get('key')

    if not key:
        return respond(400, {'error': "Missing 'key' query parameter"})

    try:
        response = table.get_item(Key={'ImageKey': key})
        item = response.get('Item')

        if not item:
            return respond(202, {'status': 'processing'})

        return respond(200, {
            'status': 'done',
            'imageKey': item['ImageKey'],
            'timestamp': int(item['Timestamp']),
            'faceCount': int(item.get('FaceCount', 0)),
            'faces': decimal_to_native(item.get('Faces', []))
        })

    except Exception as e:
        return respond(500, {'error': str(e)})


def respond(status_code, body_dict):
    return {
        'statusCode': status_code,
        'headers': {**CORS_HEADERS, 'Content-Type': 'application/json'},
        'body': json.dumps(body_dict)
    }