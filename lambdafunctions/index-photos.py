from __future__ import print_function
import boto3
import re
from decimal import Decimal
import json
import urllib
import requests
from requests_aws4auth import AWS4Auth


rekognition = boto3.client('rekognition','us-east-1')
def elastic_put(document):

    region = 'us-east-1'
    service = 'es'
    credentials = boto3.Session().get_credentials()
    awsauth = AWS4Auth(credentials.access_key, credentials.secret_key, region, service, session_token=credentials.token)

    host = 'https://search-photos-w5e3jh24pbgsw36ukysbbnnmiy.us-east-1.es.amazonaws.com'  # the Amazon ES domain, including https://
    index = 'photos'
    type = '_doc'
    url = host + '/' + index + '/' + type

    headers = {"Content-Type": "application/json"}

    r = requests.post(url, auth=awsauth, json=document, headers=headers)
    return {
        "statusCode":200,
        "message": "Photo uploaded and indexed successfully"
    }

def detect_labels(bucket, key):
    
    response = rekognition.detect_labels(Image={"S3Object": {"Bucket": bucket, "Name": key}})

    labelsArray = [str(label_prediction['Name']) for label_prediction in response['Labels']]
    #print("List of lables")
    #print(labelsArray)
    return labelsArray

def lambda_handler(event,context):
    print(event)
    s3 = boto3.client('s3')

    
    objectKey =urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'])
    #print(objectKey)
    bucket = event['Records'][0]['s3']['bucket']['name']
    createdTimestamp = event['Records'][0]['eventTime']
    # Retrieve the S3 object metadata
    metadata = s3.head_object(Bucket=bucket, Key=objectKey)
    print(metadata)
    try:
        labels = detect_labels(bucket,objectKey)
        if 'customlabels' in metadata['Metadata']:
            custom_labels = metadata['Metadata']['customlabels'].split(',')
            print(custom_labels)
            labels.extend(custom_labels)
        document = {"objectKey":objectKey, "bucket":bucket, "createdTimestamp":createdTimestamp,"labels":labels}
        elastic_put(document)
    except Exception as e:
        print(e)