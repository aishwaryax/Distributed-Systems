# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: toy_store.proto
# Protobuf Python Version: 4.25.0
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0ftoy_store.proto\x12\x08toystore\"\x1b\n\x07Request\x12\x10\n\x08ItemName\x18\x01 \x01(\t\"\x1f\n\x0b\x42uyResponse\x12\x10\n\x08Response\x18\x01 \x01(\x05\",\n\rQueryResponse\x12\x0c\n\x04\x43ost\x18\x01 \x01(\x01\x12\r\n\x05Stock\x18\x02 \x01(\x05\x32p\n\x08ToyStore\x12\x33\n\x05Query\x12\x11.toystore.Request\x1a\x17.toystore.QueryResponse\x12/\n\x03\x42uy\x12\x11.toystore.Request\x1a\x15.toystore.BuyResponseb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'toy_store_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  DESCRIPTOR._options = None
  _globals['_REQUEST']._serialized_start=29
  _globals['_REQUEST']._serialized_end=56
  _globals['_BUYRESPONSE']._serialized_start=58
  _globals['_BUYRESPONSE']._serialized_end=89
  _globals['_QUERYRESPONSE']._serialized_start=91
  _globals['_QUERYRESPONSE']._serialized_end=135
  _globals['_TOYSTORE']._serialized_start=137
  _globals['_TOYSTORE']._serialized_end=249
# @@protoc_insertion_point(module_scope)
