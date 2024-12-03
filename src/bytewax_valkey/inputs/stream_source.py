from typing import Iterable, Optional

from bytewax.inputs import FixedPartitionedSource, StatefulSourcePartition
from valkey import Valkey, from_url

from ..types import StreamRecordT

DEFAULT_BATCH_SIZE = 100


class StreamSourcePartition(StatefulSourcePartition[StreamRecordT, str]):
    def __init__(
        self,
        client: Valkey,
        stream_name: str,
        batch_size: int,
        resume_id: Optional[str] = None,
    ):
        self._client = client
        self._stream_name = stream_name.encode()
        self._resume_id = resume_id or "0-0"
        self._batch_size = batch_size

    def next_batch(self) -> Iterable[StreamRecordT]:
        payload = self._client.xread(
            streams={self._stream_name: self._resume_id},
            count=self._batch_size,
            block=0,
        )

        if not isinstance(payload, list):
            return

        for stream_name, messages in payload:
            if stream_name != self._stream_name:
                # If we got back a stream we don't expect, skip it
                continue

            # Somehow interpret these, store the latest snapshot
            for message_id, message in messages:
                self._resume_id = message_id
                yield message

    def snapshot(self) -> str:
        return self._resume_id


class StreamSource(FixedPartitionedSource[StreamRecordT, str]):
    def __init__(
        self, client: Valkey, stream_name: str, batch_size: int = DEFAULT_BATCH_SIZE
    ):
        self._client = client
        self._stream_name = stream_name
        self._batch_size = batch_size

    @classmethod
    def from_url(cls, url: str, stream_name: str, batch_size: int = DEFAULT_BATCH_SIZE):
        client = from_url(url)
        return cls(client, stream_name, batch_size)

    def list_parts(self) -> list[str]:
        return [self._stream_name]

    def build_part(
        self, step_id: str, for_part: str, resume_state: Optional[str]
    ) -> StreamSourcePartition:
        return StreamSourcePartition(
            self._client, self._stream_name, self._batch_size, resume_state
        )


__all__ = (
    "StreamSourcePartition",
    "StreamSource",
)
