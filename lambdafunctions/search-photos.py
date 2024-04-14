import json
import boto3
import requests
from requests_aws4auth import AWS4Auth
import urllib
def elastic(keywordone, keywordtwo):
    print("elastic module was called")
    region = 'us-east-1'
    service = 'es'
    credentials = boto3.Session().get_credentials()
    awsauth = AWS4Auth(credentials.access_key, credentials.secret_key, region, service, session_token=credentials.token)

    host = 'https://search-photos-w5e3jh24pbgsw36ukysbbnnmiy.us-east-1.es.amazonaws.com'
    index = 'photos'
    type = '_doc'

    url = host + '/' + index + '/_search'
    print(url)
    if keywordtwo == None:
        query = {
            "query": {
                "match": {
                    "labels": keywordone
                }
            }
        }
    else:

        query = {
            "query": {
                "bool": {
                    "should": [
                        {
                            "match": {
                                "labels": keywordone
                            }
                        },
                        {
                            "match": {
                                "labels": keywordtwo
                            }
                        }
                    ]
                }
            }
        }

    # ES 6.x requires an explicit Content-Type header
    headers = {"Content-Type": "application/json"}

    # Make the signed HTTP request
    r = requests.get(url, auth=awsauth, headers=headers, data=json.dumps(query))
    data = (r.json())
    
    n = data["hits"]["total"]["value"]
    n = int(n)
    if n == 0:
        print("No results for the query")
        return {
            "statusCode":204, # no results found
            "message":"No results"
        }
    else:
        print(n)
        Photo = [dict() for x in range(n)]
        for i in range(n):
            bucket = data["hits"]["hits"][i]["_source"]['bucket']
            objectKey = data["hits"]["hits"][i]["_source"]['objectKey']
            labels = data["hits"]["hits"][i]["_source"]['labels']
            url = "https://s3.amazonaws.com/" + bucket + "/" + objectKey
            Photo[i]['url'] = url
            Photo[i]['labels'] = labels
        SearchResponse = {}
        SearchResponse['results'] = Photo
        SearchResponse['statusCode']=200
        return SearchResponse
        

def calling_lex(query):
    client = boto3.client('lexv2-runtime',region_name='us-east-1')
    botId = "MDYZUNE2ZJ"
    botAliasId = "WRWVBOPX6U"
    localeId = "en_US"
    sessionId = "100"
    #response = client.post_text(botName='SearchPhotosChatbot', botAlias='LATEST', userId='USER', inputText=query)
    response = client.recognize_text(
    botId=botId,
    botAliasId=botAliasId,
    localeId=localeId,
    sessionId=sessionId,
    text=query)
    keyword1= None
    keyword2 = None
    if response["sessionState"]["intent"]["state"] == "ReadyForFulfillment":
        if not response["sessionState"]["intent"]["slots"]["keyword1"]:
            print("No keyword given")
            return {
            "statusCode":400, # no results found
            "message":"No keywords given"
        }
        else:
            keyword1 = response["sessionState"]["intent"]["slots"]["keyword1"]["value"]["originalValue"]
            print(keyword1)
            if response["sessionState"]["intent"]["slots"]["keyword2"] is not None:
                keyword2 = response["sessionState"]["intent"]["slots"]["keyword2"]["value"]["originalValue"]
                print(keyword2)
                
        response = elastic(keyword1, keyword2)
    else:
        response['message'] ="Inappropiate Querry"
        response['statusCode'] =400
        return {
            "statusCode":400, # no results found
            "message": "Inapproriate Query"
        }
    resp = {
      "statusCode": 200,
      "headers": {
        "Content-Type": "application/json",
        "Access-Control-Allow-Origin": "*"
      },
      "body": json.dumps(response),
      "isBase64Encoded": False
    }
    return resp

    # return response
def lambda_handler(event, context):
    # TODO implement
    # event['q']\
    print(event)
    
    query = urllib.parse.unquote_plus(event["queryStringParameters"]['q'])
    print(query)
    response = calling_lex(query)

    return response
