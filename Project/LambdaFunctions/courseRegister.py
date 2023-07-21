import boto3
import json
import re

dynamodb = boto3.resource('dynamodb')
table_name = 'Courses'

def lambda_handler(event, context):
    # Retrieve the email ID and course ID from the request body
    email_id = event['emailID']
    course_id = event['courseID']
    
    # Validate the email format
    if not validate_email(email_id):
        return {
            'statusCode': 400,
            'body': json.dumps({'message': 'Invalid email format'})
        }
    
    # Add the email ID to the set of email IDs for the course in DynamoDB
    update_email_ids(course_id, email_id)
    
    return {
        'statusCode': 200,
        'body': json.dumps({'message': 'Registered to course successfully'})
    }

def validate_email(email):
    # Regular expression pattern for email validation
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email)

def update_email_ids(course_id, email_id):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('Courses')

    response = table.update_item(
        Key={
            'courseID': course_id
        },
        UpdateExpression='ADD students :email',
        ExpressionAttributeValues={
            ':email': set([email_id])
        }
    )
