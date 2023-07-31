import boto3
import json
import re

dynamodb = boto3.resource('dynamodb')
table_name = 'Courses'
sns_client = boto3.client('sns')

def lambda_handler(event, context):
    # Retrieve the email ID and course ID from the request body
    email_id = event['emailID']
    course_id = event['courseID']
    
    # Validate the email format
    if not validate_email(email_id):
        return {
            'statusCode': 400,
            'body': 'Invalid email format'
        }
    
    # Add the email ID to the set of email IDs for the course in DynamoDB
    update_email_ids(course_id, email_id)

    # Create an SNS topic for the course_id if it doesn't exist
    topic_arn = create_sns_topic(course_id)
    
    # Subscribe the email_id to the SNS topic
    subscribe_to_topic(topic_arn, email_id)
    
    return {
        'statusCode': 200,
        'body': 'Registered to course successfully'
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

def create_sns_topic(course_id):
    topic_name = f'{course_id}'
    response = sns_client.create_topic(Name=topic_name)
    topic_arn = response['TopicArn']
    return topic_arn

def subscribe_to_topic(topic_arn, email_id):
    sns_client.subscribe(
        TopicArn=topic_arn,
        Protocol='email',
        Endpoint=email_id
    )
