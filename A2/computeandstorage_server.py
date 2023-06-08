from concurrent import futures
import logging

import grpc
import computeandstorage_pb2
import computeandstorage_pb2_grpc
import requests
import json
import urllib.parse
import boto3


class EC2Operations(computeandstorage_pb2_grpc.EC2OperationsServicer):

    def SayHello(self, request, context):
        return computeandstorage_pb2.HelloReply(message='Hello, %s!' % request.name)
    
    
    def StoreData(self,request,context):
        json_data = json.loads(request.data)
        store_json = json_data["data"]
        print('Data stored:' +store_json)
        #Logic to create s3 file and bucket

        s3 = boto3.client('s3')
        bucket_name = 'computeandstorage-grpc'
        file_path = 'computeandstorage.txt'

        s3.put_object(Bucket=bucket_name, Key=file_path, Body=store_json)

        url = s3.generate_presigned_url('get_object', Params={'Bucket': 'computeandstorage-grpc', 'Key': 'computeandstorage.txt'})

        s3_uri = {"s3uri":url}
        # s3_uri = "s3://your-bucket/your-object"
        response = computeandstorage_pb2.StoreReply(s3uri=json.dumps(s3_uri))
        return response

    def AppendData(self,request,context):
        s3 = boto3.client('s3')
        bucket_name = 'computeandstorage-grpc'
        file_path = 'computeandstorage.txt'

        response = s3.get_object(Bucket=bucket_name, Key=file_path)
        existing_data = response['Body'].read().decode('utf-8')

        json_data = json.loads(request.data)
        new_data = json_data["data"]
        updated_data = existing_data + '\n' + new_data
        s3.put_object(Bucket=bucket_name, Key=file_path, Body=updated_data)
        print("Data appended to the file in S3.")
        response = computeandstorage_pb2.AppendReply()
        return response
    
    def DeleteFile(self, request, context):
        delete_data = json.loads(request.s3uri)
        delete_url = delete_data["s3uri"]

        s3 = boto3.client('s3')
        parsed_url = urllib.parse.urlparse(delete_url)
        bucket_name = 'computeandstorage-grpc'
        # bucket_name = parsed_url.netloc
        object_key = parsed_url.path.lstrip('/')
        s3.delete_object(Bucket=bucket_name, Key=object_key)
        print("Object deleted successfully!")



def serve():
    port = '50051'
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    computeandstorage_pb2_grpc.add_EC2OperationsServicer_to_server(EC2Operations(), server)
    server.add_insecure_port('[::]:' + port)
    server.start()
    print("Server started, listening on " + port)
    server.wait_for_termination()

if __name__ == '__main__':
    logging.basicConfig()
    serve()
