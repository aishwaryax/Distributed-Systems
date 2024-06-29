from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class BuyRequest(_message.Message):
    __slots__ = ("ItemName", "Quantity")
    ITEMNAME_FIELD_NUMBER: _ClassVar[int]
    QUANTITY_FIELD_NUMBER: _ClassVar[int]
    ItemName: str
    Quantity: int
    def __init__(self, ItemName: _Optional[str] = ..., Quantity: _Optional[int] = ...) -> None: ...

class QueryRequest(_message.Message):
    __slots__ = ("ItemName",)
    ITEMNAME_FIELD_NUMBER: _ClassVar[int]
    ItemName: str
    def __init__(self, ItemName: _Optional[str] = ...) -> None: ...

class BuyResponse(_message.Message):
    __slots__ = ("Response",)
    RESPONSE_FIELD_NUMBER: _ClassVar[int]
    Response: int
    def __init__(self, Response: _Optional[int] = ...) -> None: ...

class QueryResponse(_message.Message):
    __slots__ = ("Cost", "Stock", "Name")
    COST_FIELD_NUMBER: _ClassVar[int]
    STOCK_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    Cost: float
    Stock: int
    Name: str
    def __init__(self, Cost: _Optional[float] = ..., Stock: _Optional[int] = ..., Name: _Optional[str] = ...) -> None: ...
