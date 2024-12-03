from typing import List

from bytewax.outputs import DynamicSink, StatelessSinkPartition
from valkey import Valkey, from_url


class PubSubSinkPartition(StatelessSinkPartition[bytes]):
    def __init__(self, client: Valkey, channel_id: str):
        self._client = client
        self._channel_id = channel_id

    def write_batch(self, items: List[bytes]):
        for item in items:
            self._client.publish(self._channel_id, item)


class PubSubSink(DynamicSink[bytes]):
    def __init__(self, client: Valkey, channel_id: str):
        self._client = client
        self._channel_id = channel_id

    @classmethod
    def from_url(cls, url: str, channel_id: str):
        client = from_url(url)
        return cls(client, channel_id)

    def build(
        self, step_id: str, worker_index: int, worker_count: int
    ) -> PubSubSinkPartition:
        return PubSubSinkPartition(
            self._client,
            self._channel_id,
        )


__all__ = (
    "PubSubSinkPartition",
    "PubSubSink",
)
