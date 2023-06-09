from __future__ import print_function

import logging
import json

import grpc
import computeandstorage_pb2
import computeandstorage_pb2_grpc

def run():
    # NOTE(gRPC Python Team): .close() is possible on a channel and should be
    # used in circumstances in which the with statement does not fit the needs
    # of the code.
    print("Will try to greet world ...")
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = computeandstorage_pb2_grpc.EC2OperationsStub(channel)
        response = stub.SayHello(computeandstorage_pb2.HelloRequest(name='mudra'))
        print("Greeter client received: " + response.message)

        #StoreData
        json_data = {"data":"Mudra Verma"}

        request = computeandstorage_pb2.StoreRequest(data=json.dumps(json_data))
        response = stub.StoreData(request)

        received_json = json.loads(response.s3uri)
        print(received_json["s3uri"])

        #AppendData
        append_data = {"data":"Banner ID: B00932103-00000"}
        request = computeandstorage_pb2.AppendRequest(data=json.dumps(append_data))
        response = stub.AppendData(request)

        #DeleteFile
        delete_data = {"s3uri":"https://computeandstorage-grpc.s3.amazonaws.com/computeandstorage.txt?AWSAccessKeyId=ASIAYOVUCNISNFLYAWX6&Signature=gfXQyg5MO6fOSCyrhGAR9HNoNqU%3D&x-amz-security-token=FwoGZXIvYXdzEDUaDAyJ%2FFcEcObXe6H3eiLAAW7LAUUEpMNzhAEfb0tskdyMYZqR2VfhIGEEcEdfuKb91gxaXyghFtHO8cHsOvpko3ZoFaypALxw9GNNBhkcFsHp04QJrkExB0Hu5Gs%2F3psQNJKKBDgyaUlVrUjcke85VbhtTwG4brPIFWsMb%2BKijKaIYkcp%2FE9d7aPWGjSZDL7A8WYeapdBtg6PtbPjy1xKUQsH1HX40J39LEWzm9BCkTbTbQP7JZuRxS5kLRNfHBOe%2BJoWuaDO185ITb8hMNljeSj8kIWkBjItVPHd0vc%2FYuw%2FqJeQGZ11O%2BZrV%2FSdnOI6Nq8gP6Vo9g98UKH8DsDRAL%2FhvQ9%2F&Expires=1686199071"}
        request = computeandstorage_pb2.DeleteRequest(s3uri=json.dumps(delete_data))
        response = stub.DeleteFile(request)

if __name__ == '__main__':
    logging.basicConfig()
    run()
