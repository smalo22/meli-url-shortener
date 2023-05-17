import boto3
import json

dynamodb = boto3.resource('dynamodb')
table_name = 'meli-url-shortener'

def lambda_handler(event, context):
    # Get the short ID from the user
    short_id = event['queryStringParameters']['shortid']
    
    # Check if the short ID exists in DynamoDB
    table = dynamodb.Table(table_name)
    response = table.get_item(Key={'shortid': short_id})
    
    # If the item does not exist, return a 404 error
    if 'Item' not in response:
        return {
            'statusCode': 404,
            'body': 'Short ID not found'
        }
    
    # Delete the item from DynamoDB
    table.delete_item(Key={'shortid': short_id})
    
    return {
        'statusCode': 200,
        'body': 'Item deleted successfully'
    }