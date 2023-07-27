import json
import boto3

s3 = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')
table_name = 'Courses'  # Replace with your DynamoDB table name

def lambda_handler(event, context):
    try:
        bucket_name = 'b00932103backend'  # Replace with your S3 bucket name
        file_name = 'Courses.json'  # Replace with your JSON file name

        # Fetch the JSON data from the S3 bucket
        response = s3.get_object(Bucket=bucket_name, Key=file_name)
        data = response['Body'].read().decode('utf-8')
        courses = json.loads(data)

        # Loop through the array and insert courses into the DynamoDB table
        table = dynamodb.Table(table_name)
        with table.batch_writer() as batch:
            for course in courses:
                batch.put_item(Item={
                    'courseID': course['courseID'],
                    'name': course['name'],
                    'instructor': course['instructor'],
                    'students': set(course['students']),
                    'password': course['password']
                })

        return True, 'Courses inserted successfully'
    except Exception as e:
        print('Error inserting courses:', e)
        return False, 'An error occurred while inserting courses'