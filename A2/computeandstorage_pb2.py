# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: computeandstorage.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x17\x63omputeandstorage.proto\"\x1c\n\x0cStoreRequest\x12\x0c\n\x04\x64\x61ta\x18\x01 \x01(\t\"\x1b\n\nStoreReply\x12\r\n\x05s3uri\x18\x01 \x01(\t\"\x1d\n\rAppendRequest\x12\x0c\n\x04\x64\x61ta\x18\x01 \x01(\t\"\r\n\x0b\x41ppendReply\"\x1e\n\rDeleteRequest\x12\r\n\x05s3uri\x18\x01 \x01(\t\"\r\n\x0b\x44\x65leteReply\"\x1c\n\x0cHelloRequest\x12\x0c\n\x04name\x18\x01 \x01(\t\"\x1d\n\nHelloReply\x12\x0f\n\x07message\x18\x01 \x01(\t2\xc0\x01\n\rEC2Operations\x12(\n\x08SayHello\x12\r.HelloRequest\x1a\x0b.HelloReply\"\x00\x12)\n\tStoreData\x12\r.StoreRequest\x1a\x0b.StoreReply\"\x00\x12,\n\nAppendData\x12\x0e.AppendRequest\x1a\x0c.AppendReply\"\x00\x12,\n\nDeleteFile\x12\x0e.DeleteRequest\x1a\x0c.DeleteReply\"\x00\x62\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'computeandstorage_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _STOREREQUEST._serialized_start=27
  _STOREREQUEST._serialized_end=55
  _STOREREPLY._serialized_start=57
  _STOREREPLY._serialized_end=84
  _APPENDREQUEST._serialized_start=86
  _APPENDREQUEST._serialized_end=115
  _APPENDREPLY._serialized_start=117
  _APPENDREPLY._serialized_end=130
  _DELETEREQUEST._serialized_start=132
  _DELETEREQUEST._serialized_end=162
  _DELETEREPLY._serialized_start=164
  _DELETEREPLY._serialized_end=177
  _HELLOREQUEST._serialized_start=179
  _HELLOREQUEST._serialized_end=207
  _HELLOREPLY._serialized_start=209
  _HELLOREPLY._serialized_end=238
  _EC2OPERATIONS._serialized_start=241
  _EC2OPERATIONS._serialized_end=433
# @@protoc_insertion_point(module_scope)
