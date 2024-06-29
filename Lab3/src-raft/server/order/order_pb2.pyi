from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

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

class GetRequest(_message.Message):
    __slots__ = ("OrderNumber",)
    ORDERNUMBER_FIELD_NUMBER: _ClassVar[int]
    OrderNumber: int
    def __init__(self, OrderNumber: _Optional[int] = ...) -> None: ...

class GetResponse(_message.Message):
    __slots__ = ("OrderNumber", "ToyName", "ToyQuantity")
    ORDERNUMBER_FIELD_NUMBER: _ClassVar[int]
    TOYNAME_FIELD_NUMBER: _ClassVar[int]
    TOYQUANTITY_FIELD_NUMBER: _ClassVar[int]
    OrderNumber: int
    ToyName: str
    ToyQuantity: int
    def __init__(self, OrderNumber: _Optional[int] = ..., ToyName: _Optional[str] = ..., ToyQuantity: _Optional[int] = ...) -> None: ...

class EmptyRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class IsAliveResponse(_message.Message):
    __slots__ = ("status", "orderServersId", "message")
    STATUS_FIELD_NUMBER: _ClassVar[int]
    ORDERSERVERSID_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    status: int
    orderServersId: int
    message: str
    def __init__(self, status: _Optional[int] = ..., orderServersId: _Optional[int] = ..., message: _Optional[str] = ...) -> None: ...

class NotifyReplicaRequest(_message.Message):
    __slots__ = ("orderServersId",)
    ORDERSERVERSID_FIELD_NUMBER: _ClassVar[int]
    orderServersId: int
    def __init__(self, orderServersId: _Optional[int] = ...) -> None: ...

class BoolResponse(_message.Message):
    __slots__ = ("IsSuccess",)
    ISSUCCESS_FIELD_NUMBER: _ClassVar[int]
    IsSuccess: bool
    def __init__(self, IsSuccess: bool = ...) -> None: ...

class SyncData(_message.Message):
    __slots__ = ("OrderRequests",)
    ORDERREQUESTS_FIELD_NUMBER: _ClassVar[int]
    OrderRequests: _containers.RepeatedCompositeFieldContainer[GetResponse]
    def __init__(self, OrderRequests: _Optional[_Iterable[_Union[GetResponse, _Mapping]]] = ...) -> None: ...

class DataToSyncRequest(_message.Message):
    __slots__ = ("pendingOrderStartId",)
    PENDINGORDERSTARTID_FIELD_NUMBER: _ClassVar[int]
    pendingOrderStartId: int
    def __init__(self, pendingOrderStartId: _Optional[int] = ...) -> None: ...

class LogEntry(_message.Message):
    __slots__ = ("Term", "Command")
    TERM_FIELD_NUMBER: _ClassVar[int]
    COMMAND_FIELD_NUMBER: _ClassVar[int]
    Term: int
    Command: str
    def __init__(self, Term: _Optional[int] = ..., Command: _Optional[str] = ...) -> None: ...

class AppendEntriesRequest(_message.Message):
    __slots__ = ("Term", "LeaderId", "PrevLogIndex", "PrevLogTerm", "Entries", "LeaderCommit")
    TERM_FIELD_NUMBER: _ClassVar[int]
    LEADERID_FIELD_NUMBER: _ClassVar[int]
    PREVLOGINDEX_FIELD_NUMBER: _ClassVar[int]
    PREVLOGTERM_FIELD_NUMBER: _ClassVar[int]
    ENTRIES_FIELD_NUMBER: _ClassVar[int]
    LEADERCOMMIT_FIELD_NUMBER: _ClassVar[int]
    Term: int
    LeaderId: int
    PrevLogIndex: int
    PrevLogTerm: int
    Entries: _containers.RepeatedCompositeFieldContainer[LogEntry]
    LeaderCommit: int
    def __init__(self, Term: _Optional[int] = ..., LeaderId: _Optional[int] = ..., PrevLogIndex: _Optional[int] = ..., PrevLogTerm: _Optional[int] = ..., Entries: _Optional[_Iterable[_Union[LogEntry, _Mapping]]] = ..., LeaderCommit: _Optional[int] = ...) -> None: ...

class AppendEntriesResponse(_message.Message):
    __slots__ = ("Server", "Term", "IsSuccess", "Index")
    SERVER_FIELD_NUMBER: _ClassVar[int]
    TERM_FIELD_NUMBER: _ClassVar[int]
    ISSUCCESS_FIELD_NUMBER: _ClassVar[int]
    INDEX_FIELD_NUMBER: _ClassVar[int]
    Server: int
    Term: int
    IsSuccess: bool
    Index: int
    def __init__(self, Server: _Optional[int] = ..., Term: _Optional[int] = ..., IsSuccess: bool = ..., Index: _Optional[int] = ...) -> None: ...

class RequestLogsRequest(_message.Message):
    __slots__ = ("Index", "Server")
    INDEX_FIELD_NUMBER: _ClassVar[int]
    SERVER_FIELD_NUMBER: _ClassVar[int]
    Index: int
    Server: int
    def __init__(self, Index: _Optional[int] = ..., Server: _Optional[int] = ...) -> None: ...

class CommitIndexRequest(_message.Message):
    __slots__ = ("Index",)
    INDEX_FIELD_NUMBER: _ClassVar[int]
    Index: int
    def __init__(self, Index: _Optional[int] = ...) -> None: ...
