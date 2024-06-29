# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: order.proto
# Protobuf Python Version: 4.25.1
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0border.proto\x12\x05order\"2\n\nBuyRequest\x12\x0f\n\x07ToyName\x18\x03 \x01(\t\x12\x13\n\x0bToyQuantity\x18\x02 \x01(\x05\"3\n\x0b\x42uyResponse\x12\x13\n\x0bOrderNumber\x18\x02 \x01(\x05\x12\x0f\n\x07Message\x18\x01 \x01(\t\"!\n\nGetRequest\x12\x13\n\x0bOrderNumber\x18\x01 \x01(\x05\"H\n\x0bGetResponse\x12\x13\n\x0bOrderNumber\x18\x01 \x01(\x05\x12\x0f\n\x07ToyName\x18\x02 \x01(\t\x12\x13\n\x0bToyQuantity\x18\x03 \x01(\x05\"\x0e\n\x0c\x45mptyRequest\"J\n\x0fIsAliveResponse\x12\x0e\n\x06status\x18\x01 \x01(\x05\x12\x16\n\x0eorderServersId\x18\x02 \x01(\x05\x12\x0f\n\x07message\x18\x03 \x01(\t\".\n\x14NotifyReplicaRequest\x12\x16\n\x0eorderServersId\x18\x02 \x01(\x05\"!\n\x0c\x42oolResponse\x12\x11\n\tIsSuccess\x18\x01 \x01(\x08\"5\n\x08SyncData\x12)\n\rOrderRequests\x18\x01 \x03(\x0b\x32\x12.order.GetResponse\"0\n\x11\x44\x61taToSyncRequest\x12\x1b\n\x13pendingOrderStartId\x18\x01 \x01(\x05\x32\x91\x03\n\x05Order\x12\x31\n\x08\x62uyOrder\x12\x11.order.BuyRequest\x1a\x12.order.BuyResponse\x12\x31\n\x08GetOrder\x12\x11.order.GetRequest\x1a\x12.order.GetResponse\x12\x36\n\x07IsAlive\x12\x13.order.EmptyRequest\x1a\x16.order.IsAliveResponse\x12\x41\n\rNotifyReplica\x12\x1b.order.NotifyReplicaRequest\x1a\x13.order.BoolResponse\x12\x38\n\x10SynchronizeOrder\x12\x0f.order.SyncData\x1a\x13.order.BoolResponse\x12\x34\n\x08IsLeader\x12\x13.order.EmptyRequest\x1a\x13.order.BoolResponse\x12\x37\n\nDataToSync\x12\x18.order.DataToSyncRequest\x1a\x0f.order.SyncDatab\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'order_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  DESCRIPTOR._options = None
  _globals['_BUYREQUEST']._serialized_start=22
  _globals['_BUYREQUEST']._serialized_end=72
  _globals['_BUYRESPONSE']._serialized_start=74
  _globals['_BUYRESPONSE']._serialized_end=125
  _globals['_GETREQUEST']._serialized_start=127
  _globals['_GETREQUEST']._serialized_end=160
  _globals['_GETRESPONSE']._serialized_start=162
  _globals['_GETRESPONSE']._serialized_end=234
  _globals['_EMPTYREQUEST']._serialized_start=236
  _globals['_EMPTYREQUEST']._serialized_end=250
  _globals['_ISALIVERESPONSE']._serialized_start=252
  _globals['_ISALIVERESPONSE']._serialized_end=326
  _globals['_NOTIFYREPLICAREQUEST']._serialized_start=328
  _globals['_NOTIFYREPLICAREQUEST']._serialized_end=374
  _globals['_BOOLRESPONSE']._serialized_start=376
  _globals['_BOOLRESPONSE']._serialized_end=409
  _globals['_SYNCDATA']._serialized_start=411
  _globals['_SYNCDATA']._serialized_end=464
  _globals['_DATATOSYNCREQUEST']._serialized_start=466
  _globals['_DATATOSYNCREQUEST']._serialized_end=514
  _globals['_ORDER']._serialized_start=517
  _globals['_ORDER']._serialized_end=918
# @@protoc_insertion_point(module_scope)