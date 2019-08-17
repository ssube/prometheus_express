# prometheus_express

A Prometheus SDK for CircuitPython/MicroPython boards.

- only depends on `socket`
- API-compatible with [prometheus/client_python](https://github.com/prometheus/client_python)
- not terribly slow (`wrk` reports upwards of 100rps with 2 metrics)

## Supported Features

### HTTP

This module implements a very rudimentary HTTP server that likely violates some part of the spec. However, it works
with Chrome, curl, and Prometheus itself.

Call `start_http_server(port)` to bind a socket and begin listening.

Call `await_http_request(server, registry)` to await an incoming HTTP request and respond with the metrics in
`registry`. As 

## Metric Types

Currently, `Counter` and `Gauge` are the only metric types implemented.

### Counter

Both `inc` and `dec` are implemented.

### Gauge

Extends [counter](#counter) with `set`.

### Labels

Labels are not yet implemented.

## Known Issues

### Load Causes OSError

Load testing the HTTP endpoint may cause one of a variety of `OSError`s, often `errno` 3, 4, or 7.

Not sure what is causing the errors, but it is not predictable and may not appear immediately:

```shell
> ./wrk -c 1 -d 60s -t 1 http://server:8080/
Running 1m test @ http://server:8080/
  1 threads and 1 connections
^C  Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency     8.64ms  485.57us  12.81ms   97.75%
    Req/Sec   111.60      5.21   121.00     71.00%
  2222 requests in 20.61s, 671.83KB read
  Socket errors: connect 0, read 1, write 2743, timeout 0
Requests/sec:    107.82
Transfer/sec:     32.60KB
```

Some are fatal:

```
Connection from ('client', 8080)
Accepting...
Connection from ('client', 8080)
Accepting...
Error accepting request: [Errno 128] ENOTCONN
Binding: server:8080
Traceback (most recent call last):
  File "code.py", line 90, in <module>
  File "code.py", line 87, in main
  File "code.py", line 87, in main
  File "code.py", line 55, in bind
  File "/lib/prometheus_express/http.py", line 11, in start_http_server
OSError: 4
```

Others require the socket to be rebound:

```
Connection from ('10.2.1.193', 8080)
Accepting...
Error accepting request: 7
Binding: 10.2.2.136:8080
Accepting...
```
