# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: order.proto
# Protobuf Python Version: 4.25.0
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0border.proto\x12\x05order\"2\n\nBuyRequest\x12\x0f\n\x07ToyName\x18\x03 \x01(\t\x12\x13\n\x0bToyQuantity\x18\x02 \x01(\x05\"3\n\x0b\x42uyResponse\x12\x13\n\x0bOrderNumber\x18\x02 \x01(\x05\x12\x0f\n\x07Message\x18\x01 \x01(\t2:\n\x05Order\x12\x31\n\x08\x62uyOrder\x12\x11.order.BuyRequest\x1a\x12.order.BuyResponseb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'order_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  DESCRIPTOR._options = None
  _globals['_BUYREQUEST']._serialized_start=22
  _globals['_BUYREQUEST']._serialized_end=72
  _globals['_BUYRESPONSE']._serialized_start=74
  _globals['_BUYRESPONSE']._serialized_end=125
  _globals['_ORDER']._serialized_start=127
  _globals['_ORDER']._serialized_end=185
# @@protoc_insertion_point(module_scope)
