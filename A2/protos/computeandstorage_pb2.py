# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: protos/computeandstorage.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x1eprotos/computeandstorage.proto\x12\x11\x63omputeandstorage\"\x1c\n\x0cStoreRequest\x12\x0c\n\x04\x64\x61ta\x18\x01 \x01(\t\"\x1b\n\nStoreReply\x12\r\n\x05s3uri\x18\x01 \x01(\t\"\x1d\n\rAppendRequest\x12\x0c\n\x04\x64\x61ta\x18\x01 \x01(\t\"\r\n\x0b\x41ppendReply\"\x1e\n\rDeleteRequest\x12\r\n\x05s3uri\x18\x01 \x01(\t\"\r\n\x0b\x44\x65leteReply2\x82\x02\n\rEC2Operations\x12M\n\tStoreData\x12\x1f.computeandstorage.StoreRequest\x1a\x1d.computeandstorage.StoreReply\"\x00\x12P\n\nAppendData\x12 .computeandstorage.AppendRequest\x1a\x1e.computeandstorage.AppendReply\"\x00\x12P\n\nDeleteFile\x12 .computeandstorage.DeleteRequest\x1a\x1e.computeandstorage.DeleteReply\"\x00\x62\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'protos.computeandstorage_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _STOREREQUEST._serialized_start=53
  _STOREREQUEST._serialized_end=81
  _STOREREPLY._serialized_start=83
  _STOREREPLY._serialized_end=110
  _APPENDREQUEST._serialized_start=112
  _APPENDREQUEST._serialized_end=141
  _APPENDREPLY._serialized_start=143
  _APPENDREPLY._serialized_end=156
  _DELETEREQUEST._serialized_start=158
  _DELETEREQUEST._serialized_end=188
  _DELETEREPLY._serialized_start=190
  _DELETEREPLY._serialized_end=203
  _EC2OPERATIONS._serialized_start=206
  _EC2OPERATIONS._serialized_end=464
# @@protoc_insertion_point(module_scope)
