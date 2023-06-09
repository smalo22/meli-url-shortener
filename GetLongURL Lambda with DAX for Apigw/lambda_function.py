import boto3
import json
import amazondax

dynamodb = boto3.resource('dynamodb')
dax = amazondax.AmazonDaxClient.resource(endpoint_url='daxs://melidaxv2.bsag9w.dax-clusters.us-east-1.amazonaws.com')
table_name = 'meli-url-shortener'

def lambda_handler(event, context):
    # Get the short ID from the user
    short_id = event['pathParameters']['shortid']
    #short_id = event['shortid']
    #return print(event)
    
    # Retrieve the long URL from DynamoDB
    table = dax.Table(table_name)
    #table = dynamodb.Table(table_name)
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
            'body': 'La URL corta que usted ha introducido no se ha encontrado.'
        }