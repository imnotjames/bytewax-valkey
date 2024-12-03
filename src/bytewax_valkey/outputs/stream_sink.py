from typing import Any, List, cast

from bytewax.outputs import DynamicSink, StatelessSinkPartition
from valkey import Valkey, from_url

from ..types import StreamRecordT

DEFAULT_BATCH_SIZE = 100


class StreamSinkPartition(StatelessSinkPartition[StreamRecordT]):
    def __init__(
        self,
        client: Valkey,
        stream_name: str,
    ):
        self._client = client
        self._stream_name = stream_name.encode()

    def write_batch(self, items: List[StreamRecordT]):
        for item in items:
            # Because of the current typing of valkey library, `xadd`
            # fields type is incompatible with this `StreamRecordT`.
            #
            # For the time being we can cast this as `Any` to avoid
            # the typing as we're pretty confident this type is correct.
            item = cast(Any, item)
            self._client.xadd(self._stream_name, item)


class StreamSink(DynamicSink[StreamRecordT]):
    def __init__(self, client: Valkey, stream_name: str):
        self._client = client
        self._stream_name = stream_name

    @classmethod
    def from_url(cls, url: str, stream_name: str):
        client = from_url(url)
        return cls(client, stream_name)

    def list_parts(self) -> list[str]:
        return [self._stream_name]

    def build(
        self, step_id: str, worker_index: int, worker_count: int
    ) -> StreamSinkPartition:
        return StreamSinkPartition(self._client, self._stream_name)


__all__ = (
    "StreamSinkPartition",
    "StreamSink",
)
