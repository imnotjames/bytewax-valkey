[![PyPI](https://img.shields.io/pypi/v/bytewax-valkey.svg?style=flat-square)][pypi-package]

# Bytewax Valkey

[Valkey][valkey] connectors for [Bytewax][bytewax].

This connector offers 3 sources and 2 sinks:

* `StreamSink` - writes [Valkey streams][valkey-streams] using `xadd`
* `StreamSource` - reads [Valkey streams][valkey-streams] using `xread`
* `PubSubSink` - writes [Valkey pubsub][valkey-pubsub] using `publish`
* `PubSubSource` - reads [Valkey pubsub][valkey-pubsub] using `subscribe`
* `PubSubPatternSource` - reads [Valkey pubsub][valkey-pubsub] using `psubscribe`

## Installation

This package is available via [PyPi][pypi-package] as
`bytewax-valkey` and can be installed via your package manager of choice.

## Usage

### Pub/Sub Source

```python
import os

from bytewax_valkey import PubSubSource
from bytewax.connectors.stdio import StdOutSink

import bytewax.operators as op
from bytewax.dataflow import Dataflow

VALKEY_URL = os.environ["VALKEY_URL"]

flow = Dataflow("valkey_example")
flow_input = op.input("input", flow, PubSubSource.from_url(VALKEY_URL, "example"))
op.output("output", flow_input, StdOutSink())
```

### Pub/Sub Pattern Source

```python
import os

from bytewax_valkey import PubSubPatternSource
from bytewax.connectors.stdio import StdOutSink

import bytewax.operators as op
from bytewax.dataflow import Dataflow

VALKEY_URL = os.environ["VALKEY_URL"]

flow = Dataflow("valkey_example")
flow_input = op.input("input", flow, PubSubPatternSource.from_url(VALKEY_URL, "example*"))
op.output("output", flow_input, StdOutSink())
```

### Pub/Sub Sink

```python
import os

from bytewax_valkey import PubSubSink
from bytewax.testing import TestingSource

import bytewax.operators as op
from bytewax.dataflow import Dataflow

VALKEY_URL = os.environ["VALKEY_URL"]

flow = Dataflow("valkey_example")
flow_input = op.input("input", flow, TestingSource([b"example message"]))
op.output("output", flow_input, PubSubSink.from_url(VALKEY_URL, "example"))
```

### Stream Source

```python
import os

from bytewax_valkey import StreamSource
from bytewax.connectors.stdio import StdOutSink

import bytewax.operators as op
from bytewax.dataflow import Dataflow

VALKEY_URL = os.environ["VALKEY_URL"]

flow = Dataflow("valkey_example")
flow_input = op.input("input", flow, StreamSource.from_url(VALKEY_URL, "example"))
op.output("output", flow_input, StdOutSink())
```

### Stream Sink

```python
import os

from bytewax_valkey import StreamSink
from bytewax.testing import TestingSource

import bytewax.operators as op
from bytewax.dataflow import Dataflow

VALKEY_URL = os.environ["VALKEY_URL"]

flow = Dataflow("valkey_example")
flow_input = op.input("input", flow, TestingSource([{"key": "value"}]))
op.output("output", flow_input, StreamSink.from_url(VALKEY_URL, "example"))
```

## License

Licensed under the [MIT License](./LICENSE).

[valkey]: https://valkey.io
[bytewax]: https://bytewax.io
[valkey-streams]: https://valkey.io/topics/streams-intro/
[valkey-pubsub]: https://valkey.io/topics/pubsub/
[pypi-package]: https://pypi.org/project/bytewax-valkey