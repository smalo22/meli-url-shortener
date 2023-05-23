import json
import random
import string
import boto3

dynamodb = boto3.resource('dynamodb')
table_name = 'meli-url-shortener'
base_url = 'https://sm-it.click/'

def generate_short_id():
    return ''.join((random.choice(string.ascii_lowercase + string.digits) for _ in range(8)))

def lambda_handler(event, context):
    # Get the long URL from the user
    long_url = event['long_url']
    #print("Your URL is: " + long_url)
    
    # Check if the long URL already exists in DynamoDB
    table = dynamodb.Table(table_name)
    response = table.scan(FilterExpression=boto3.dynamodb.conditions.Attr('longurl').eq(long_url))
    
    if response['Items']:
        # If the long URL already exists, return the existing short ID
        short_id = response['Items'][0]['shortid']
        message = f"La URL larga que ha pegado ya existe en Nuestra DB. Esta es su URL corta: {base_url}{short_id}"
    else:
        while True:
            # Generate a random short ID
            short_id = generate_short_id()
            
            # Check if the short ID already exists in DynamoDB
            response = table.get_item(Key={'shortid': short_id})
            if 'Item' not in response:
                # If the short ID doesn't exist, store the values in DynamoDB and break the loop
                table.put_item(Item={'shortid': short_id, 'longurl': long_url})
                break
        
        message = f"Esta es su URL corta: {base_url}{short_id}"
    
    response = {
        'statusCode': 200,
        'body': message
    }
    
    return response
