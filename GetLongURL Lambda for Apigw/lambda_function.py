import boto3
import json

dynamodb = boto3.resource('dynamodb')
table_name = 'meli-url-shortener'

def lambda_handler(event, context):
    # Get the short ID from the user
    short_id = event['pathParameters']['shortid']
    #short_id = event['shortid']
    
    # Retrieve the long URL from DynamoDB
    table = dynamodb.Table(table_name)
    response = table.get_item(Key={'shortid': short_id})
    
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