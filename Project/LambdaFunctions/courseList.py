import boto3

def lambda_handler(event, context):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('Courses')
    
    # Scan the table to retrieve all items
    response = table.scan()
    items = response.get('Items', [])
    
    # Prepare the course details
    course_details = []
    for item in items:
        course = {
            'courseID': item['courseID'],
            'name': item['name'],
            'instructor': item['instructor']
        }
        course_details.append(course)
    
    return {
        'statusCode': 200,
        'body': course_details
    }
