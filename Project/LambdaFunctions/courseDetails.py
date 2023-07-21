import boto3
import json

def lambda_handler(event, context):
    # Retrieve the course ID from the event
    course_id = event['courseID']
    
    # Fetch course details from DynamoDB
    course_details = get_course_details(course_id)
    
    if course_details:
        # Convert set to list before serialization
        course_details['students'] = list(course_details['students'])
        
        return course_details  # Return the JSON object directly
    else:
        return {
            'statusCode': 404,
            'body': json.dumps({'message': 'Course not found'})
        }

def get_course_details(course_id):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('Courses')
    
    response = table.get_item(
        Key={
            'courseID': course_id
        }
    )
    item = response.get('Item', None)
    
    return item
