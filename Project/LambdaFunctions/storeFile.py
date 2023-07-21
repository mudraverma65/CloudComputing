import boto3

dynamodb = boto3.resource('dynamodb')
table_name = 'Notes'

def lambda_handler(event, context):
    # Retrieve the course ID, lecture name, and file URL from the event
    course_id = event['courseID']
    lecture_name = event['lectureName']
    file_url = event['fileURL']
    
    # Create an item in DynamoDB
    table = dynamodb.Table(table_name)
    table.put_item(
        Item={
            'courseID': course_id,
            'fileURL': file_url,
            'lectureName': lecture_name
        }
    )
    
    return {
        'statusCode': 200,
        'body': 'Item created in DynamoDB'
    }
