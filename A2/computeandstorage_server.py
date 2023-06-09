from concurrent import futures
import logging

import grpc
import computeandstorage_pb2
import computeandstorage_pb2_grpc
import json
import urllib.parse
import boto3
import requests

# from flask import Flask, request, jsonify   

# app = Flask(__name__)

class EC2Operations(computeandstorage_pb2_grpc.EC2OperationsServicer):

    def __init__(self):
        access_key = 'ASIAYOVUCNISBG4GCSPE'
        secret_key = 'C7CP2vXJh+CZ9QFtZYTQn7f5HqNXGUnEQclqoUE3'
        session_token = 'FwoGZXIvYXdzEE0aDLc24iocTi2e/yFeeSLAARxHauOuyJ6sNI+uMqvaQnzuGB4uS5Mm0iZohndlkRw6w9KXGpVL1BoWMPmH40AuP5kXMtHUSaqf5F+SvvV+RvS2xdFh9cCPIqSDla7uXLOHiU/U0wFLtNCvOjgnqQUJgxZdN4BqnB+J6we0SyFsbs6nOhfRVkg1BFBAT/USJo6mZjcQzYbJwprt+QrBSp9XqYHbUnYYGsubo9csIJ+QqBOf7BzizWlazzCG/tTCKY5JbnpUoZN3lu9GCFqkN0Trlij4uYqkBjItsJ3wx+0wB1Qqv2Oz0UglvEPT2fFkaDAvEPy+TVhgxeWBIc479pkDKvRD7XEB'

        session = boto3.Session(
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
            aws_session_token=session_token
        )
        self.s3 = session.client('s3') 
        # self.s3 = boto3.client('s3')

    def SayHello(self, request, context):
        return computeandstorage_pb2.HelloReply(message='Hello, %s!' % request.name)
    
    # @app.route('/storedata', methods=['POST'])
    def StoreData(self,request,context):
        json_data = json.loads(request.data)
        store_json = json_data["data"]
        print('Data stored:' +store_json)
        #Logic to create s3 file and bucket

        # s3 = boto3.client('s3')
        bucket_name = 'computeandstorage-grpc'
        file_path = 'computeandstorage.txt'

        self.s3.put_object(Bucket=bucket_name, Key=file_path, Body=store_json)

        url = self.s3.generate_presigned_url('get_object', Params={'Bucket': 'computeandstorage-grpc', 'Key': 'computeandstorage.txt'})

        s3_uri = {"s3uri":url}
        response = computeandstorage_pb2.StoreReply(s3uri=json.dumps(s3_uri))
        return response

    def AppendData(self,request,context):
        # s3 = boto3.client('s3')
        bucket_name = 'computeandstorage-grpc'
        file_path = 'computeandstorage.txt'

        response = self.s3.get_object(Bucket=bucket_name, Key=file_path)
        existing_data = response['Body'].read().decode('utf-8')

        json_data = json.loads(request.data)
        new_data = json_data["data"]
        updated_data = existing_data + '\n' + new_data
        self.s3.put_object(Bucket=bucket_name, Key=file_path, Body=updated_data)
        print("Data appended to the file in S3.")
        response = computeandstorage_pb2.AppendReply()
        return response
    
    def DeleteFile(self, request, context):
        delete_data = json.loads(request.s3uri)
        delete_url = delete_data["s3uri"]

        # s3 = boto3.client('s3')
        parsed_url = urllib.parse.urlparse(delete_url)
        bucket_name = 'computeandstorage-grpc'
        object_key = parsed_url.path.lstrip('/')

        self.s3.delete_object(Bucket=bucket_name, Key=object_key)
        print("Object deleted successfully!")
        response = computeandstorage_pb2.DeleteReply()
        return response

def sendPost():
    url = 'http://54.173.209.76:9000/start'

    payload = {
        "banner": "B00932103",
        "ip": "54.227.85.166"
    }

    headers = {'Content-Type': 'application/json'}

    try:
        response = requests.post(url, data=json.dumps(payload), headers=headers)
        response.raise_for_status()
        print('Start request sent successfully!')
    except requests.exceptions.RequestException as e:
        print('Error sending start request:', str(e))


def serve():
    port = '0'
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    computeandstorage_pb2_grpc.add_EC2OperationsServicer_to_server(EC2Operations(), server)
    # server.add_insecure_port('[::]:' + port)
    # server.add_insecure_port('54.227.85.166:' + port)
    server.add_insecure_port('0.0.0.0:' + port)
    server.start()
    print("Server started, listening on " + port)
    # print("asasas")
    sendPost()
    server.wait_for_termination()
    
    

if __name__ == '__main__':
    logging.basicConfig()
    serve()
