import boto3
import json
import amazondax

dax_endpoint = 'daxs://meli.bsag9w.dax-clusters.us-east-1.amazonaws.com'
table_name = 'meli-url-shortener'

dax = amazondax.AmazonDaxClient.resource(endpoint_url=dax_endpoint)

def lambda_handler(event, context):
    # Extract the path from the event object
    path = event['rawPath']
    
    # Remove the first character of the path
    path = path[1:]
    
    # Retrieve the long URL from DynamoDB DAX
    table = dax.Table(table_name)
    response = table.get_item(Key={'shortid': path})
    
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