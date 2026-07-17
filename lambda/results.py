"""
Emotion Recognition Upload API - accepts a base64 webcam snapshot
and uploads it to S3, which triggers the detection pipeline.
"""

import base64
import json
import os
import time
import uuid

import boto3

s3_client = boto3.client('s3')
BUCKET_NAME = os.environ['BUCKET_NAME']

CORS_HEADERS = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Allow-Methods': 'OPTIONS,POST'
}


def lambda_handler(event, context):
    try:
        body = json.loads(event.get('body') or '{}')
        image_base64 = body.get('image')
        filename = body.get('filename')

        if not image_base64:
            return respond(400, {'error': "Missing 'image' (base64 string) in request body"})

        if image_base64.startswith('data:'):
            image_base64 = image_base64.split(',', 1)[1]

        image_bytes = base64.b64decode(image_base64)

        if not filename:
            filename = f"snapshot-{uuid.uuid4().hex}.jpg"

        key = f"webcam-snapshots/{int(time.time())}-{filename}"

        s3_client.put_object(
            Bucket=BUCKET_NAME,
            Key=key,
            Body=image_bytes,
            ContentType='image/jpeg'
        )

        return respond(200, {'message': 'Snapshot uploaded successfully', 'bucket': BUCKET_NAME, 'key': key})

    except Exception as e:
        print(f"Upload error: {e}")
        return respond(500, {'error': str(e)})


def respond(status_code, body_dict):
    return {
        'statusCode': status_code,
        'headers': {**CORS_HEADERS, 'Content-Type': 'application/json'},
        'body': json.dumps(body_dict)
    }