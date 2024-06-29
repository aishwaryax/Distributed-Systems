from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class Request(_message.Message):
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
    __slots__ = ("Cost", "Stock")
    COST_FIELD_NUMBER: _ClassVar[int]
    STOCK_FIELD_NUMBER: _ClassVar[int]
    Cost: float
    Stock: int
    def __init__(self, Cost: _Optional[float] = ..., Stock: _Optional[int] = ...) -> None: ...
