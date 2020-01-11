# prometheus_express

A [Prometheus](https://prometheus.io/) SDK for CircuitPython and MicroPython boards, helping integrate I2C and SPI
sensors into existing Prometheus monitoring infrastructure.

- only depends on `socket`
- runs on CircuitPython 4.x and MicroPython for ESP32 and M0/M4 devices
- runs even faster on CPython 3.x for local testing
- API compatible with the official [prometheus/client_python](https://github.com/prometheus/client_python)
- basic HTTP server with path/method routing
- not terribly slow (20 rps on an ESP32, 50 rps on an M4 core, 5k on an i7 core)

For those unfamiliar with Prometheus, the examples expose an HTTP server on port `:8080` that serves `/metrics` in
a readable, plaintext format:

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

The Prometheus server will occasionally scrape each device, collecting sensor readings with metadata about
their source, and passing the samples on to [long-term storage](https://github.com/ssube/prometheus-sql-adapter/).

## Contents

- [prometheus_express](#prometheusexpress)
  - [Contents](#contents)
  - [Status](#status)
  - [Releases](#releases)
  - [Supported Hardware](#supported-hardware)
  - [Supported Features](#supported-features)
    - [HTTP Server](#http-server)
    - [Metric Labels](#metric-labels)
    - [Metric Types](#metric-types)
      - [Counter](#counter)
      - [Gauge](#gauge)
      - [Summary](#summary)
    - [Registries](#registries)
  - [Planned Features](#planned-features)
  - [Known Issues](#known-issues)
    - [OSError 3, 4, or 7](#oserror-3-4-or-7)
    - [OSError 112](#oserror-112)

## Status

[![Pipeline Status](https://git.apextoaster.com/ssube/prometheus_express/badges/master/pipeline.svg)](https://git.apextoaster.com/ssube/prometheus_express/commits/master)
[![Test Coverage](https://codecov.io/gh/ssube/prometheus_express/branch/master/graph/badge.svg)](https://codecov.io/gh/ssube/prometheus_express)
[![MIT license](https://img.shields.io/github/license/ssube/prometheus_express.svg)](https://github.com/ssube/prometheus_express/blob/master/LICENSE.md)

[![Open bug count](https://img.shields.io/github/issues-raw/ssube/prometheus_express/type-bug.svg)](https://github.com/ssube/prometheus_express/issues?q=is%3Aopen+is%3Aissue+label%3Atype%2Fbug)
[![Open issue count](https://img.shields.io/github/issues-raw/ssube/prometheus_express.svg)](https://github.com/ssube/prometheus_express/issues?q=is%3Aopen+is%3Aissue)
[![Closed issue count](https://img.shields.io/github/issues-closed-raw/ssube/prometheus_express.svg)](https://github.com/ssube/prometheus_express/issues?q=is%3Aissue+is%3Aclosed)

[![Maintainability](https://api.codeclimate.com/v1/badges/0b84df4baf76afa1b4c4/maintainability)](https://codeclimate.com/github/ssube/prometheus_express/maintainability)
[![Technical debt ratio](https://img.shields.io/codeclimate/tech-debt/ssube/prometheus_express)](https://codeclimate.com/github/ssube/prometheus_express/trends/technical_debt)
[![Quality issues](https://img.shields.io/codeclimate/issues/ssube/prometheus_express)](https://codeclimate.com/github/ssube/prometheus_express/issues)
[![LGTM Language grade: Python](https://img.shields.io/lgtm/grade/python/g/ssube/prometheus_express.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/ssube/prometheus_express/context:python)
[![LGTM Total alerts](https://img.shields.io/lgtm/alerts/g/ssube/prometheus_express.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/ssube/prometheus_express/alerts/)

## Releases

[![github release link](https://img.shields.io/badge/github-release-blue?logo=github)](https://github.com/ssube/prometheus_express/releases)
[![github release version](https://img.shields.io/github/tag/ssube/prometheus_express.svg)](https://github.com/ssube/prometheus_express/releases)
[![github commits since release](https://img.shields.io/github/commits-since/ssube/prometheus_express/v0.0.4.svg)](https://github.com/ssube/prometheus_express/compare/v0.0.4...master)

[![PyPI release link](https://img.shields.io/badge/pypi-package-blue?logo=pypi)](https://github.com/ssube/prometheus_express/releases)
[![PyPI release version](https://img.shields.io/pypi/v/prometheus_express?color=green)](https://pypi.org/project/prometheus-express/)

## Supported Hardware

This library is tested on:

- the [Adafruit Feather M4 Express](https://www.adafruit.com/product/3857) running MicroPython 4.1.0 or better,
  with an [Adafruit Ethernet FeatherWing](https://www.adafruit.com/product/3201) attached (using the Wiznet5500
  driver).
- the [Olimex ESP32-POE](https://www.olimex.com/Products/IoT/ESP32/ESP32-POE/open-source-hardware) running
  CircuitPython 1.12.0 or better, with wifi or wired ethernet (using the LAN8720 driver)

## Supported Features

### HTTP Server

This module implements a very rudimentary HTTP server that almost certainly violates some part of the spec.
However, it works with Chrome, curl, and Prometheus itself. Depending on the platform, it may also work with
`wrk` benchmarks ([known issues](#known-issues)).

### Metric Labels

Labels are stored and used to accumulate values. Missing labels are reported as `None`.

If a metric is constructed with labels, a default entry with all values set to `None` will also be reported.

### Metric Types

`Counter`, `Gauge`, and `Summary` are implemented with labels.

#### Counter

Incremental values. Implements `inc(value)` and `dec(value)`.

#### Gauge

Absolute values. Extends [counter](#counter) with `set(value)`.

#### Summary

Individual values. Prints count and total of `observe(value)`.

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
- tests for API compatibility

## Known Issues

### OSError 3, 4, or 7

Load testing the HTTP endpoint may cause one of a variety of `OSError`s, often `errno` 3, 4, or 7.

[This is related to the Wiznet5500 driver](https://github.com/adafruit/circuitpython/issues/2073) for
ethernet FeatherWings, and may not appear on other devices:

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

```none
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

```none
Connection from ('client', 8080)
Accepting...
Error accepting request: 7
Binding: server:8080
Accepting...
```

### OSError 112

Certain crashes may leak open sockets, causing the device to log an `OSError 112` during startup.

The error prevents the HTTP server from binding to the ethernet device, so an HTTP watchdog on the
switch can be used to restart POE devices. The board can also be reset by calling `machine.reset()`
from the REPL.
