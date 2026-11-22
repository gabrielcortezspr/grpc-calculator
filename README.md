# gRPC Calculator

![Python](https://img.shields.io/badge/Python-3.9+-3776AB?logo=python&logoColor=white)
![gRPC](https://img.shields.io/badge/gRPC-Protocol%20Buffers-244c5a?logo=google&logoColor=white)
[![tests](https://github.com/gabrielcortezspr/grpc-calculator/actions/workflows/tests.yml/badge.svg)](https://github.com/gabrielcortezspr/grpc-calculator/actions/workflows/tests.yml)
![License](https://img.shields.io/badge/license-MIT-green)

A distributed calculator built with **gRPC** and **Protocol Buffers** in Python. A stateless
server exposes `Add`, `Sub`, `Mul` and `Div` as unary RPCs, with **server interceptors** for
request logging and input validation. Built as a Distributed Systems course project by
Gabriel Cortez and Italo Monte.

## Highlights

- **Contract-first API:** the service is defined in [`proto/calculator.proto`](proto/calculator.proto);
  Python stubs are generated with `grpc_tools.protoc`.
- **Interceptors:** `LoggingInterceptor` traces every call (method, request, response) and
  `ValidationInterceptor` rejects division by zero with `INVALID_ARGUMENT` before it reaches
  the handler.
- **Stateless and concurrent:** no state between calls, served by a 10-worker thread pool.
- **Tested three ways:** automated test runner (spins the server up and down), a Python client
  with an interactive mode, and `grpcurl` scripts. The runner also measures throughput.

## Architecture

```
┌──────────────┐   OperationRequest {a, b}   ┌──────────────────────────────────────┐
│  client.py   │ ──────────────────────────► │ server.py  :50051                    │
│  grpcurl     │ ◄────────────────────────── │  LoggingInterceptor                  │
└──────────────┘  OperationResponse          │  ValidationInterceptor (b == 0 → ✗)  │
                  {result, success, error}   │  CalculatorService: Add Sub Mul Div  │
                                             └──────────────────────────────────────┘
```

## Getting started

```bash
pip install -r requirements.txt

# (optional) regenerate the stubs after editing the .proto
python -m grpc_tools.protoc -I proto --python_out=generated --grpc_python_out=generated proto/calculator.proto

python server/server.py                    # terminal 1: server on port 50051
python client/client.py                    # terminal 2: runs the predefined operations
python client/client.py --interactive      # or type operations by hand
```

With [grpcurl](https://github.com/fullstorydev/grpcurl):

```bash
grpcurl -plaintext -import-path proto -proto calculator.proto \
  -d '{"a": 10, "b": 5}' localhost:50051 calculator.CalculatorService/Div
```

## Tests

```bash
python tests/test_runner.py    # starts the server, runs the suite, stops the server
./tests/test_grpcurl.sh        # same scenarios through grpcurl
```

Covers the four operations, decimal and negative operands, division by zero rejected by the
interceptor, and a 100-call throughput check. The suite runs on every push through GitHub
Actions.

Sample server log:

```
INFO - Starting unary call: /calculator.CalculatorService/Add
INFO - Request received: a: 10.0 b: 5.0
INFO - Addition: 10.0 + 5.0 = 15.0
INFO - Unary call finished: /calculator.CalculatorService/Add
```

(The actual log messages are in Portuguese.)

## Project structure

```
├── proto/calculator.proto   # service contract
├── generated/               # protoc output (calculator_pb2*.py)
├── server/server.py         # service implementation + interceptors
├── client/client.py         # test client, automatic and interactive modes
├── tests/                   # test runner and grpcurl script
├── docs/video-script.md     # presentation script (Portuguese)
└── setup.sh                 # installs dependencies and regenerates the stubs
```

## References

- [gRPC Python documentation](https://grpc.io/docs/languages/python/)
- [Protocol Buffers](https://protobuf.dev/)
- [gRPC interceptors](https://grpc.io/docs/guides/interceptors/)

## License

[MIT](LICENSE)
