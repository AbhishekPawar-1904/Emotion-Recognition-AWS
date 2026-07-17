"""
Emotion Recognition - Lambda Function
Flow: Webcam snapshot -> Upload API -> S3 -> SQS -> this Lambda
      -> Rekognition DetectFaces (emotions) -> DynamoDB + CloudWatch metrics
"""

import json
import os
import time
import urllib.parse
from decimal import Decimal

import boto3

rekognition_client = boto3.client('rekognition')
cloudwatch_client = boto3.client('cloudwatch')
dynamodb = boto3.resource('dynamodb')

MIN_CONFIDENCE = float(os.environ.get('MIN_CONFIDENCE', '70'))
NAMESPACE = os.environ.get('CLOUDWATCH_NAMESPACE', 'EmotionRecognition')
RESULTS_TABLE = os.environ['RESULTS_TABLE']

results_table = dynamodb.Table(RESULTS_TABLE)


def lambda_handler(event, context):
    batch_item_failures = []

    for sqs_record in event['Records']:
        try:
            s3_event = json.loads(sqs_record['body'])
            for s3_record in s3_event.get('Records', []):
                bucket = s3_record['s3']['bucket']['name']
                key = urllib.parse.unquote_plus(s3_record['s3']['object']['key'])
                process_image(bucket, key)
        except Exception as e:
            print(f"Failed to process SQS message {sqs_record.get('messageId')}: {e}")
            batch_item_failures.append({'itemIdentifier': sqs_record['messageId']})

    return {'batchItemFailures': batch_item_failures}


def process_image(bucket, key):
    response = rekognition_client.detect_faces(
        Image={'S3Object': {'Bucket': bucket, 'Name': key}},
        Attributes=['ALL']
    )

    face_details = response.get('FaceDetails', [])
    timestamp = int(time.time())
    faces_result = []

    for idx, face in enumerate(face_details):
        emotions = face.get('Emotions', [])
        # Sort emotions by confidence, take the strongest one as the "primary" emotion
        emotions_sorted = sorted(emotions, key=lambda e: e['Confidence'], reverse=True)
        top_emotion = emotions_sorted[0] if emotions_sorted else None

        all_emotions = {
            e['Type']: round(e['Confidence'], 2)
            for e in emotions_sorted if e['Confidence'] >= MIN_CONFIDENCE
        }

        face_data = {
            'faceIndex': idx,
            'primaryEmotion': top_emotion['Type'] if top_emotion else 'UNKNOWN',
            'primaryConfidence': round(top_emotion['Confidence'], 2) if top_emotion else 0,
            'allEmotions': all_emotions,
            'ageRangeLow': face.get('AgeRange', {}).get('Low'),
            'ageRangeHigh': face.get('AgeRange', {}).get('High')
        }
        faces_result.append(face_data)

    print(f"Image: {key} -> Faces detected: {len(faces_result)} -> {json.dumps(faces_result)}")

    # Push CloudWatch metrics: count per primary emotion type
    metric_data = []
    for face in faces_result:
        metric_data.append({
            'MetricName': 'EmotionDetectionCount',
            'Dimensions': [{'Name': 'EmotionType', 'Value': face['primaryEmotion']}],
            'Timestamp': time.time(),
            'Value': 1,
            'Unit': 'Count'
        })
    if metric_data:
        cloudwatch_client.put_metric_data(Namespace=NAMESPACE, MetricData=metric_data)

    # Store result in DynamoDB (convert floats to Decimal for storage)
    results_table.put_item(
        Item={
            'ImageKey': key,
            'Bucket': bucket,
            'Timestamp': timestamp,
            'FaceCount': len(faces_result),
            'Faces': json.loads(json.dumps(faces_result), parse_float=Decimal)
        }
    )

    return faces_result
