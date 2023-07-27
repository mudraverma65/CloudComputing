import boto3
import json

def lambda_handler(event, context):
    # Retrieve the course code and password from the event directly
    try:
        courseID = event['courseID']
        password = event['password']
    except KeyError:
        return {
            'statusCode': 400,
            'body': 'Invalid request format'
        }
    
    # Authenticate the course code and password against the DynamoDB table
    if authenticate_course(courseID, password):
        # Successful login
        return {
            'statusCode': 200,
            'body': 'Login successful'
        }
    else:
        # Invalid credentials
        return {
            'statusCode': 401,
            'body': 'Invalid credentials'
        }

def authenticate_course(courseID, password):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('Courses')

    # Query the DynamoDB table to check if the course code and password match
    response = table.get_item(
        Key={
            'courseID': courseID
        }
    )
    item = response.get('Item', None)

    if item and item['password'] == password:
        # Course code and password match
        return True
    else:
        # Invalid course code or password
        return False