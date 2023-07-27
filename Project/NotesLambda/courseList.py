import boto3
import json

s3 = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Courses')

def insert_courses():
    try:
        bucket_name = 'b00932103backend'  # Replace with your S3 bucket name
        file_name = 'Courses.json'  # Replace with your JSON file name

        # Fetch the JSON data from the S3 bucket
        response = s3.get_object(Bucket=bucket_name, Key=file_name)
        data = response['Body'].read().decode('utf-8')
        courses = json.loads(data)

        # Loop through the array and insert courses into the DynamoDB table
        table = dynamodb.Table('Courses')
        with table.batch_writer() as batch:
            for course in courses:
                batch.put_item(Item={
                    'courseID': course['courseID'],
                    'name': course['name'],
                    'instructor': course['instructor'],
                    'students': set(course['students']),
                    'password': course['password']
                })

        return True
    except Exception as e:
        print('Error inserting courses:', e)
        return False

def lambda_handler(event, context):
    # dynamodb = boto3.resource('dynamodb')
    # table = dynamodb.Table('Courses')
    
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
        
    if not course_details:
        # If the course_details list is empty, execute insert_courses()
        success = insert_courses()
        
        if success:
            # Fetch the course details again after inserting
            response = table.scan()
            items = response.get('Items', [])
            for item in items:
                course = {
                    'courseID': item['courseID'],
                    'name': item['name'],
                    'instructor': item['instructor']
                }
                course_details.append(course)
    
    return course_details
