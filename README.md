# prometheus_express

A [Prometheus](https://prometheus.io/) SDK for CircuitPython/MicroPython boards, allowing sensor data to be integrated
into existing Prometheus/Grafana monitoring infrastructure.

- only depends on `socket`
- runs on CircuitPython 4.x for embedded devices
- runs on CPython 3.x for local testing
- API compatible with the official [prometheus/client_python](https://github.com/prometheus/client_python)
- basic HTTP server with path/method routing
- not terribly slow (`wrk` reports upwards of 10 rps with routing)

For those unfamiliar with Prometheus, the examples expose an HTTP server on port `:8080` that reports metrics in a
plaintext format:

```none
# HELP prom_express_gas gas from the bme680 sensor
# TYPE prom_express_gas gauge
prom_express_gas 1060948
# HELP prom_express_humidity humidity from both sensors
# TYPE prom_express_humidity gauge
prom_express_humidity{sensor="None"} 0
prom_express_humidity{sensor="bme680"} 49.4062
prom_express_humidity{sensor="si7021"} 49.7976
# HELP prom_express_pressure pressure from the bme680 sensor
# TYPE prom_express_pressure gauge
prom_express_pressure 983.25
# HELP prom_express_temperature temperature from both sensors
# TYPE prom_express_temperature gauge
prom_express_temperature{sensor="None"} 0
prom_express_temperature{sensor="bme680"} 24.7359
prom_express_temperature{sensor="si7021"} 24.3325
```

## Contents

- [prometheus_express](#prometheusexpress)
  - [Contents](#contents)
  - [Status](#status)
  - [Releases](#releases)
  - [Supported Hardware](#supported-hardware)
  - [Supported Features](#supported-features)
    - [HTTP](#http)
    - [Labels](#labels)
    - [Metric Types](#metric-types)
      - [Counter](#counter)
      - [Gauge](#gauge)
      - [Summary](#summary)
    - [Registries](#registries)
  - [Planned Features](#planned-features)
  - [Known Issues](#known-issues)
    - [Load Causes OSError](#load-causes-oserror)

## Status

[![Pipeline Status](https://git.apextoaster.com/ssube/prometheus_express/badges/master/pipeline.svg)](https://git.apextoaster.com/ssube/prometheus_express/commits/master)
[![Test Coverage](https://codecov.io/gh/ssube/prometheus_express/branch/master/graph/badge.svg)](https://codecov.io/gh/ssube/prometheus_express)
[![MIT license](https://img.shields.io/github/license/ssube/prometheus_express.svg)](https://github.com/ssube/prometheus_express/blob/master/LICENSE.md)

[![Open bug count](https://img.shields.io/github/issues-raw/ssube/prometheus_express/type-bug.svg)](https://github.com/ssube/prometheus_express/issues?q=is%3Aopen+is%3Aissue+label%3Atype%2Fbug)
[![Open issue count](https://img.shields.io/github/issues-raw/ssube/prometheus_express.svg)](https://github.com/ssube/prometheus_express/issues?q=is%3Aopen+is%3Aissue)
[![Closed issue count](https://img.shields.io/github/issues-closed-raw/ssube/prometheus_express.svg)](https://github.com/ssube/prometheus_express/issues?q=is%3Aissue+is%3Aclosed)

## Releases

[![github release link](https://img.shields.io/badge/github-release-blue?logo=github)](https://github.com/ssube/prometheus_express/releases)
[![github release version](https://img.shields.io/github/tag/ssube/prometheus_express.svg)](https://github.com/ssube/prometheus_express/releases)
[![github commits since release](https://img.shields.io/github/commits-since/ssube/prometheus_express/v0.0.3.svg)](https://github.com/ssube/prometheus_express/compare/v0.0.3...master)

![PyPI](https://img.shields.io/pypi/v/prometheus_express?color=green)

## Supported Hardware

This library is developed for the [Adafruit Feather M4 Express](https://www.adafruit.com/product/3857) running
MicroPython 4.1.0 or better, with an [Adafruit Ethernet FeatherWing](https://www.adafruit.com/product/3201) attached.

## Supported Features

### HTTP

This module implements a very rudimentary HTTP server that likely violates some part of the spec. However, it works
with Chrome, curl, and Prometheus itself.

### Labels

Labels are not yet implemented.

### Metric Types

`Counter`, `Gauge`, and `Summary` are implemented with labels.

#### Counter

Incremental values. Implements `inc(value)` and `dec(value)`.

#### Gauge

Absolute values. Extends [counter](#counter) with `set(value)`.

#### Summary

Prints count and total of `observe(value)`.

### Registries

Registries may be created with a namespace: `CollectorRegistry(namespace='foo')`

Call `registry.render()` to format metrics in Prometheus'
[plain text exposition format](https://prometheus.io/docs/instrumenting/exposition_formats/#text-based-format):

```none
# HELP prom_express_test_counter a test counter
# TYPE prom_express_test_counter counter
prom_express_test_counter 1588
# HELP prom_express_test_gauge a test gauge
# TYPE prom_express_test_gauge gauge
prom_express_test_gauge 3887
```

Metrics may be registered with multiple registries.

## Planned Features

- push support: `push_to_gateway`
- remaining metric types: `Histogram`

## Known Issues

### Load Causes OSError

Load testing the HTTP endpoint may cause one of a variety of `OSError`s, often `errno` 3, 4, or 7.

Not sure what is causing the errors, but it is not predictable and may not appear immediately:

```shell
> ./wrk -c 1 -d 60s -t 1 http://server:8080/
Running 1m test @ http://server:8080/
  1 threads and 1 connections
    Thread Stats   Avg      Stdev     Max   +/- Stdev
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
Connection from ('client', 8080)
Accepting...
Error accepting request: 7
Binding: server:8080
Accepting...
```
