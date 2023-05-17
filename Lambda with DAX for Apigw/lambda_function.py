import boto3
import json
import amazondax

dynamodb = boto3.resource('dynamodb')
dax = amazondax.AmazonDaxClient(resource_arn='arn:aws:dax:us-east-1:707810240585:cache/meli', endpoints=['daxs://meli.bsag9w.dax-clusters.us-east-1.amazonaws.com'])
table_name = 'meli-url-shortener'

def lambda_handler(event, context):
    # Get the short ID from the user
    short_id = event['pathParameters']['shortid']
    #short_id = event['shortid']
    #return print(event)
    
    # Retrieve the long URL from DynamoDB
    table = dynamodb.Table(table_name)
    #response = table.get_item(Key={'shortid': short_id})
    response = dax.table(table_name).get_item(Key={'shortid': short_id})
    
    # Check if the item exists in the table
    if 'Item' in response:
        long_url = response['Item']['longurl']
        return {
            'statusCode': 301,
            'headers': {
                'Location': long_url
            },
            'body': ''
        }
    else:
        return {
            'statusCode': 404,
            'body': 'Short ID not found'
        }
