[![PyPI](https://img.shields.io/pypi/v/bytewax-valkey.svg?style=flat-square)][pypi-package]

# Bytewax Lever

[Valkey][valkey] connectors for [Bytewax][bytewax].

This connector offers 1 source and 1 sink:

* `StreamSource` - reads [Valkey streams][valkey-streams] using `xread`
* `PubSubSource` - writes [Valkey pubsub][valkey-pubsub] using `subscribe`

## Installation

This package is available via [PyPi][pypi-package] as
`bytewax-valkey` and can be installed via your package manager of choice.

## Usage

### Pub/Sub Source

```python
import os

from bytewax_valkey.inputs.pubsub_source import PubSubSource
from bytewax.connectors.stdio import StdOutSink

import bytewax.operators as op
from bytewax.dataflow import Dataflow

VALKEY_URL = os.environ["VALKEY_URL"]

flow = Dataflow("valkey_example")
flow_input = op.input("input", flow, PubSubSource.from_url(VALKEY_URL, "example"))
op.output("output", flow_input, StdOutSink())

```

### Stream Source

```python
import os

from bytewax_valkey.inputs.stream_source import StreamSource
from bytewax.connectors.stdio import StdOutSink

import bytewax.operators as op
from bytewax.dataflow import Dataflow

VALKEY_URL = os.environ["VALKEY_URL"]

flow = Dataflow("valkey_example")
flow_input = op.input("input", flow, StreamSource.from_url(VALKEY_URL, "example"))
op.output("output", flow_input, StdOutSink())

```

## License

Licensed under the [MIT License](./LICENSE).

[valkey]: https://valkey.io
[bytewax]: https://bytewax.io
[valkey-streams]: https://valkey.io/topics/streams-intro/
[valkey-pubsub]: https://valkey.io/topics/pubsub/
[pypi-package]: https://pypi.org/project/bytewax-valkey