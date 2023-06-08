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
        json_data = {"data":"Mudra Verma A2"}

        request = computeandstorage_pb2.StoreRequest(data=json.dumps(json_data))
        response = stub.StoreData(request)

        received_json = json.loads(response.s3uri)
        print(received_json["s3uri"])
        # s3_uri = response.s3uri
        # print(f"S3 URI: {s3_uri}")

        #AppendData
        append_data = {"data":"Mudra Verma A2"}


if __name__ == '__main__':
    logging.basicConfig()
    run()
