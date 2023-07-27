import sys
import traceback
import logging
import json
import boto3
from urllib.parse import unquote_plus, quote

logger = logging.getLogger()
logger.setLevel(logging.INFO)
sns_client = boto3.client('sns')


def lambda_handler(event, context):
    textract = boto3.client("textract")
    s3 = boto3.client("s3")
    
    try:
        if "Records" in event:
            file_obj = event["Records"][0]
            bucketName = str(file_obj["s3"]["bucket"]["name"])
            fileName = unquote_plus(str(file_obj["s3"]["object"]["key"]))
            
            # Check if the object key contains the excluded folder path
            if "output" in fileName:
                return {
                    'statusCode': 200,
                    'body': 'Skipped processing for the excluded folder'
                }
            
            courseID = fileName.split("/")[0]

            logging.info(f"Bucket: {bucketName} ::: Course: {courseID} ::: Key: {fileName}")

            response = textract.detect_document_text(
                Document={
                    "S3Object": {
                        "Bucket": bucketName,
                        "Name": fileName,
                    }
                }
            )
            logging.info(json.dumps(response))

            # change LINE by WORD if you want word level extraction
            raw_text = extract_text(response, extract_by="LINE")
            logging.info(raw_text)

            s3.put_object(
                Bucket=bucketName,
                Key=f"output/{courseID}/{fileName.split('/')[-1]}.txt",
                Body=str("\n".join(raw_text)),
            )
            
            topic_arn = create_sns_topic(courseID)
            
            file_url = f"https://{bucketName}.s3.amazonaws.com/output/{fileName}.txt"
            
            message = f"Notes have been uploaded. \nFile Link:\n{file_url}"
            
            publish_message(topic_arn, message)

            return {
                'statusCode': 200,
                'body': 'Document processed successfully!'
            }
    except:
        error_msg = process_error()
        logger.error(error_msg)

    return {
        'statusCode': 500, 
        'body': 'Error processing the document!'
    }
    
def process_error() -> dict:
    ex_type, ex_value, ex_traceback = sys.exc_info()
    traceback_string = traceback.format_exception(ex_type, ex_value, ex_traceback)
    error_msg = json.dumps(
        {
            "errorType": ex_type.__name__,
            "errorMessage": str(ex_value),
            "stackTrace": traceback_string,
        }
    )
    return error_msg


def extract_text(response: dict, extract_by="LINE") -> list:
    text = []
    for block in response["Blocks"]:
        if block["BlockType"] == extract_by:
            text.append(block["Text"])
    return text
    
def create_sns_topic(topic_name):
    response = sns_client.create_topic(Name=topic_name)
    topic_arn = response['TopicArn']
    return topic_arn
    
def publish_message(courseID, message):
    sns_client.publish(TopicArn=courseID, Message=message)