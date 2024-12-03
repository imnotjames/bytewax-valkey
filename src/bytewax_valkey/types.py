from typing import Mapping, TypeAlias, TypeVar

StreamFieldT = TypeVar("StreamFieldT", bytes, str, memoryview)
StreamValueT = TypeVar("StreamValueT", int, float, bytes, str, memoryview)
StreamRecordT: TypeAlias = Mapping[StreamFieldT, StreamValueT]

__all__ = (
    "StreamFieldT",
    "StreamValueT",
    "StreamRecordT",
)
