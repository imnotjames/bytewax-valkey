import pytest
from pytest_mock import MockerFixture, MockType
from valkey import Valkey

from bytewax_valkey.inputs.pubsub_source import PubSubSource, PubSubSourcePartition


@pytest.fixture(autouse=True)
def mock_from_url(mocker: MockerFixture):
    yield mocker.patch("bytewax_valkey.inputs.pubsub_source.from_url")


@pytest.fixture()
def mock_valkey(mocker: MockerFixture):
    yield mocker.create_autospec(spec=Valkey)


class TestPubSubSource:
    @pytest.fixture(autouse=True)
    def mock_partition(self, mocker: MockerFixture):
        yield mocker.patch("bytewax_valkey.inputs.pubsub_source.PubSubSourcePartition")

    def test_from_url_calls_from_url(
        self, mock_from_url: MockType, mock_partition: MockType
    ):
        source = PubSubSource.from_url("valkey://example/0", "channel")

        mock_from_url.assert_called_once_with("valkey://example/0")

        source.build("step", 0, 1)

        mock_partition.assert_called_once_with(mock_from_url.return_value, "channel")


class TestPubSubSourcePartition:
    def test_creates_pubsub_from_client(self, mock_valkey: MockType):
        PubSubSourcePartition(mock_valkey, "example")

        mock_valkey.pubsub.assert_called_once()
        mock_valkey.pubsub.return_value.subscribe.assert_called_once_with("example")

    def test_next_batch_listens_to_first_item(self, mock_valkey: MockType):
        partition = PubSubSourcePartition(mock_valkey, "example")

        mock_pubsub = mock_valkey.pubsub.return_value
        mock_pubsub.listen.return_value = [
            {"type": "message", "data": b"example 1"},
            {"type": "message", "data": b"example 2"},
        ]

        actual = partition.next_batch()

        assert actual == [b"example 1"]

    def test_next_batch_ignores_other_events(self, mock_valkey: MockType):
        partition = PubSubSourcePartition(mock_valkey, "example")

        mock_pubsub = mock_valkey.pubsub.return_value
        mock_pubsub.listen.return_value = [
            {"type": "other", "data": b"other"},
            {"type": "message", "data": b"example 1"},
        ]

        actual = partition.next_batch()

        assert actual == [b"example 1"]

    def test_next_batch_ignores_missing_data(self, mock_valkey: MockType):
        partition = PubSubSourcePartition(mock_valkey, "example")

        mock_pubsub = mock_valkey.pubsub.return_value
        mock_pubsub.listen.return_value = [
            {"type": "message", "data": None},
            {"type": "message", "data": b"example 1"},
        ]

        actual = partition.next_batch()

        assert actual == [b"example 1"]
