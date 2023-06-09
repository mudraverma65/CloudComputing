"""
Name: Mudra Verma
Banner ID: B00932103
CSCI5409 - Compute & Storage Assignment
"""

from concurrent import futures
import logging

import grpc
from protos import computeandstorage_pb2
from protos import computeandstorage_pb2_grpc
import urllib.parse
import boto3

class EC2Operations_Implementation(computeandstorage_pb2_grpc.EC2OperationsServicer):
    
    def StoreData(self,request, context):
        store_json = request.data
        print('Data stored:' +store_json)
        
        # Create an S3 client
        s3 = boto3.client('s3')
        bucket_name = 'b0092103-csci5409-a2'
        file_path = 'computeandstorage.txt'

        # Store the data in the S3 bucket
        s3.put_object(Bucket=bucket_name, Key=file_path, Body=store_json)

        # Generate a pre-signed URL to access the stored object
        url = s3.generate_presigned_url('get_object', Params={'Bucket': 'b0092103-csci5409-a2', 'Key': 'computeandstorage.txt'})

        # Create and return the response with the pre-signed URL
        response = computeandstorage_pb2.StoreReply(s3uri=url)
        return response    

    def AppendData(self,request,context):
        # Create an S3 client
        s3 = boto3.client('s3')
        bucket_name = 'b0092103-csci5409-a2'
        file_path = 'computeandstorage.txt'

        # Retrieve the existing data from the S3 bucket
        response = s3.get_object(Bucket=bucket_name, Key=file_path)
        existing_data = response['Body'].read().decode()
        
        # Retrieve the new data from the request
        new_data = request.data

        # Append the new data to the existing data
        updated_data = existing_data + new_data

        # Update the object in the S3 bucket with the updated data
        s3.put_object(Bucket=bucket_name, Key=file_path, Body=updated_data.encode())
    
        # Create and return the response
        response = computeandstorage_pb2.AppendReply()
        return response
    
    
    def DeleteFile(self, request, context):
        # Retrieve the delete URL from the request
        delete_url = request.s3uri

        # Create an S3 client
        s3 = boto3.client('s3')
        parsed_url = urllib.parse.urlparse(delete_url)
        bucket_name = 'b0092103-csci5409-a2'
        object_key = parsed_url.path.lstrip('/')

        # Delete the object from the S3 bucket
        s3.delete_object(Bucket=bucket_name, Key=object_key)

        # Create and return the response
        response = computeandstorage_pb2.DeleteReply()
        return response


def serve():
    port = '50051'
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

    # Add the EC2OperationsServicer implementation to the server
    computeandstorage_pb2_grpc.add_EC2OperationsServicer_to_server(EC2Operations_Implementation(), server)
    server.add_insecure_port('[::]:' + port)
    server.start()
    print("Server started, listening on " + port)
    server.wait_for_termination()    
    

if __name__ == '__main__':
    logging.basicConfig()
    serve()
