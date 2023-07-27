import boto3

dynamodb = boto3.resource('dynamodb')
table_name = 'Notes'

def lambda_handler(event, context):
    # Retrieve the course ID, lecture name, and file URL from the event
    course_id = event['courseID']
    lecture_no = event['lectureNo']
    file_url = event['fileURL']
    
    # Create an item in DynamoDB
    table = dynamodb.Table(table_name)
    table.put_item(
        Item={
            'courseID': course_id,
            'lectureNo': lecture_no,
            'fileURL': file_url
        }
    )
    
    return {
        'statusCode': 200,
        'body': 'Item created in DynamoDB'
    }
