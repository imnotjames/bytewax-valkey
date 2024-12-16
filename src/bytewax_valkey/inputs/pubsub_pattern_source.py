from typing import Iterable

from bytewax.inputs import DynamicSource, StatelessSourcePartition
from valkey import Valkey, from_url


class PubSubPatternSourcePartition(StatelessSourcePartition[tuple[bytes, bytes]]):
    def __init__(self, client: Valkey, pattern: str | bytes):
        self._pubsub = client.pubsub()
        self._pubsub.psubscribe(pattern)

    def next_batch(self) -> Iterable[tuple[bytes, bytes]]:
        for message in self._pubsub.listen():
            if message["type"] != "pmessage":
                continue

            if not isinstance(message["data"], bytes):
                continue

            return [(message["channel"], message["data"])]

        return []

    def close(self):
        self._pubsub.close()


class PubSubPatternSource(DynamicSource[tuple[bytes, bytes]]):
    def __init__(self, client: Valkey, pattern: bytes | str):
        self._client = client
        self._pattern = pattern

    @classmethod
    def from_url(cls, url: str, pattern: bytes | str):
        client = from_url(url)
        return cls(client, pattern)

    def build(
        self, step_id: str, worker_index: int, worker_count: int
    ) -> PubSubPatternSourcePartition:
        return PubSubPatternSourcePartition(self._client, self._pattern)
