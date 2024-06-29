from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class BuyRequest(_message.Message):
    __slots__ = ("ToyName", "ToyQuantity")
    TOYNAME_FIELD_NUMBER: _ClassVar[int]
    TOYQUANTITY_FIELD_NUMBER: _ClassVar[int]
    ToyName: str
    ToyQuantity: int
    def __init__(self, ToyName: _Optional[str] = ..., ToyQuantity: _Optional[int] = ...) -> None: ...

class BuyResponse(_message.Message):
    __slots__ = ("OrderNumber", "Message")
    ORDERNUMBER_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    OrderNumber: int
    Message: str
    def __init__(self, OrderNumber: _Optional[int] = ..., Message: _Optional[str] = ...) -> None: ...
