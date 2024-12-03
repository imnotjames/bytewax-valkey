from typing import Iterable

from bytewax.inputs import DynamicSource, StatelessSourcePartition
from valkey import Valkey, from_url


class PubSubSourcePartition(StatelessSourcePartition[bytes]):
    def __init__(self, client: Valkey, channel_id: str):
        self._pubsub = client.pubsub()
        self._pubsub.subscribe(channel_id)

    def next_batch(self) -> Iterable[bytes]:
        for message in self._pubsub.listen():
            if message["type"] != "message":
                continue

            if not isinstance(message["data"], bytes):
                continue

            return [message["data"]]

        return []

    def close(self):
        self._pubsub.close()


class PubSubSource(DynamicSource[bytes]):
    def __init__(self, client: Valkey, channel_id: str):
        self._client = client
        self._channel_id = channel_id

    @classmethod
    def from_url(cls, url: str, channel_id: str):
        client = from_url(url)
        return cls(client, channel_id)

    def build(
        self, step_id: str, worker_index: int, worker_count: int
    ) -> PubSubSourcePartition:
        return PubSubSourcePartition(
            self._client,
            self._channel_id,
        )


__all__ = (
    "PubSubSourcePartition",
    "PubSubSource",
)
