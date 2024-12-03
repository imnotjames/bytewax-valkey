from typing import Mapping, TypeVar, TypeAlias

StreamFieldT = TypeVar("StreamFieldT", bytes, str, memoryview)
StreamValueT = TypeVar("StreamValueT", int, float, bytes, str, memoryview)
StreamRecordT: TypeAlias = Mapping[StreamFieldT, StreamValueT]

__all__ = (
    "StreamFieldT",
    "StreamValueT",
    "StreamRecordT",
)
