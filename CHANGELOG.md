# Changelog

All notable changes to this project will be documented in this file. See [standard-version](https://github.com/conventional-changelog/standard-version) for commit guidelines.

### [0.0.4](https://github.com/ssube/prometheus_express/compare/v0.0.3...v0.0.4) (2019-12-27)


### Features

* **registry:** provide render handler ([9fc6dbc](https://github.com/ssube/prometheus_express/commit/9fc6dbc00125657425ce7fb335a4bcf66ad2ba79))


### Bug Fixes

* **docs:** link pypi badge to package ([72a5b0b](https://github.com/ssube/prometheus_express/commit/72a5b0b0a5114b4b8c9c2b848b32650b8be03aef))
* **examples:** handle parsing errors in minimal ([9623e42](https://github.com/ssube/prometheus_express/commit/9623e42cbafe4732c8e9338b2a3858bdb8bf67a5))
* **examples:** remove duplicate import from cpython ([91cf326](https://github.com/ssube/prometheus_express/commit/91cf3261da7ef6c35b83bcfded09fa8d623546ba))
* **metric:** handle dec correctly when no value exists for labels ([a3dcea1](https://github.com/ssube/prometheus_express/commit/a3dcea1bc437740b08f8d1240f4d68842b69ffc5))
* **metric:** only print help/type once for summaries ([ad58e32](https://github.com/ssube/prometheus_express/commit/ad58e32d9113a9fee28c5adf09e1478e49954697))
* **router:** register new routes correctly ([74da839](https://github.com/ssube/prometheus_express/commit/74da839daa7f4f8ef5502f0a9bc92b156c720a16))
* **server:** ensure complete http header is present ([efa6694](https://github.com/ssube/prometheus_express/commit/efa66943e30971f809c7db0dd9772019480f0415))
* **test:** decode response chunks in mock ([e6e959b](https://github.com/ssube/prometheus_express/commit/e6e959bad3d5537b4ef68a0432e959fff8616fb1))
* **test:** encode mock conn responses ([b8da77b](https://github.com/ssube/prometheus_express/commit/b8da77b2d56b77af569e03b831cdc9dd3f1e573e))

### 0.0.3 (2019-12-25)


### ⚠ BREAKING CHANGES

* **metric:** validate names according to Prometheus data model rules.
ValueError will be raised for invalid names that would have previously been accepted.
* rename all print/print_* methods to render/render_*
to be more compatible with Python 3
* **server:** server.await_http_request renamed to Server.accept
* **router:** http file renamed to server, route to router

### Features

* **build:** add a build, run tests with coverage ([6d8ade4](https://github.com/ssube/prometheus_express/commit/6d8ade4f61e595477aeac8aa0bd31bbb13f270b6))
* **build:** add climate/codecov targets to make ([4303d1b](https://github.com/ssube/prometheus_express/commit/4303d1bc97d93ffb39b39459b459db25b4d0743b))
* **build:** add commit status and coverage upload jobs ([0d9af01](https://github.com/ssube/prometheus_express/commit/0d9af01d1b6d534049a44a411de6b7295173c9c1))
* **build:** emit and artifact html coverage report ([7d153bf](https://github.com/ssube/prometheus_express/commit/7d153bfce1edb8e06fe242fa587ee6ed15e17c28))
* **examples:** add bme680 sensor to i2c example ([c66b2fe](https://github.com/ssube/prometheus_express/commit/c66b2fe2f52ea12ed7dcb9c0c26474769d0b83b9))
* **examples:** add example parser, clean up bind ([4791718](https://github.com/ssube/prometheus_express/commit/479171876dd910ea6f4e3b52f4fb543e2286387c))
* **examples:** add example with i2c sensor (si7021 temperature/humidity) ([f9ea0e4](https://github.com/ssube/prometheus_express/commit/f9ea0e4515abbe3877f397d8a0b866f54035e750))
* **examples:** use labels in i2c example (fixes [#1](https://github.com/ssube/prometheus_express/issues/1)) ([57c2938](https://github.com/ssube/prometheus_express/commit/57c2938b34da15e5a371cbeba32a607a5f7c3f80))
* **metric:** naive implementation of labels for all types ([1cec4a2](https://github.com/ssube/prometheus_express/commit/1cec4a212d96f1f788d0241c7527f1d7caab85df))
* **metric:** validate metric and label names (fixes [#2](https://github.com/ssube/prometheus_express/issues/2)) ([f6057e5](https://github.com/ssube/prometheus_express/commit/f6057e596fa2609819619951aeeb9805f99e0f64))
* **metrics:** add summary metric type ([2b5dba6](https://github.com/ssube/prometheus_express/commit/2b5dba6b9f222eb6d1adb2a7ec4c7f5c0fb79183))
* **router:** implement (method, path) routing ([ce967b7](https://github.com/ssube/prometheus_express/commit/ce967b7deceeaa98bc82bdc3bdcc0ff5359a86e7))
* **scripts:** add github status script ([29e5027](https://github.com/ssube/prometheus_express/commit/29e50279e0433e3e7e3dfeb79f92282387755042))
* **scripts:** add rudimentary deploy script for lib+example ([1bf14b1](https://github.com/ssube/prometheus_express/commit/1bf14b1424a8cc742359d8675eb233bd5fc708b7))
* **server:** make depth and timeout parameters, get request body from parse method ([9b983f9](https://github.com/ssube/prometheus_express/commit/9b983f959b44da1c11eb4f27d5623dc24f3593b5))
* **server:** set socket timeout if possible ([46f632e](https://github.com/ssube/prometheus_express/commit/46f632e0ef01f321549275743f81ccbcad624978))
* **utils:** add bind helper ([1f1f862](https://github.com/ssube/prometheus_express/commit/1f1f8624cad3fe8768d504d1cafcc69c62f79823))
* **utils:** move i2c scan into utils ([81c591e](https://github.com/ssube/prometheus_express/commit/81c591e90139c2126a0832598064e440168fef66))
* **utils:** supported limited number of i2c lock tries ([173168c](https://github.com/ssube/prometheus_express/commit/173168c70f7a9143271f21a369bbb6924f2c0559))
* add example for normal python too ([db3fd98](https://github.com/ssube/prometheus_express/commit/db3fd98b6ebac496d0c7ee8efe9b6c7695e83ad0))
* add package structure ([4eb9e92](https://github.com/ssube/prometheus_express/commit/4eb9e928fc6fdde3436c778d97df3785f31b57b6))
* implement basic path routing ([f29e276](https://github.com/ssube/prometheus_express/commit/f29e2763e87c7de618fd23d15f6bc5d2951c5fe7))
* prometheus sdk for circuitpython ([26b88e3](https://github.com/ssube/prometheus_express/commit/26b88e364ada8265795b8bf85421cac4458e1288))


### Bug Fixes

* **build:** generate xml coverage report for codeclimate ([496b974](https://github.com/ssube/prometheus_express/commit/496b97473ad991d57d6836fa4397b6bd866b5d66))
* **docs:** readme badges ([4e9216e](https://github.com/ssube/prometheus_express/commit/4e9216e0d5f53315f12ea1a81274fbbffd0e822d))
* **examples:** clean up networking ([f098c6b](https://github.com/ssube/prometheus_express/commit/f098c6bcd6553b989121a674be4b8d1264aaef2f))
* **examples:** poll for IP more slowly, print any errors after accept ([2fe23d9](https://github.com/ssube/prometheus_express/commit/2fe23d9013e2fce586dcf220dac7ce98c3a67fe9))
* **examples:** update with render calls ([2e87fca](https://github.com/ssube/prometheus_express/commit/2e87fcac2672561130b6dc3778afbfa926d0c42b))
* **examples:** use lambda handlers ([ec0b275](https://github.com/ssube/prometheus_express/commit/ec0b275694411e4ddd02db5865af27f93ee719af))
* **examples:** working cpython/linux example ([f10a124](https://github.com/ssube/prometheus_express/commit/f10a1247bc538a4fe4c6c49df594fcab41519484))
* **metric:** include namespace in counter value line ([f8cdc8e](https://github.com/ssube/prometheus_express/commit/f8cdc8e29b709c8e4663f73542f323f74fa03c45))
* **metric:** omit label brackets when no labels are present ([39887bb](https://github.com/ssube/prometheus_express/commit/39887bbeb07c63503cd6f792cfa0032c72b364d0))
* **metric:** reset labels after receiving a value ([21564fa](https://github.com/ssube/prometheus_express/commit/21564fa8522fb1213070db3b969964502611f00b))
* **server:** block with timeout on cpython ([3498c2a](https://github.com/ssube/prometheus_express/commit/3498c2a378832d2d773e41d6b15c42f86265a0ff))
* **test:** cover label and registry render more ([f0f5bc8](https://github.com/ssube/prometheus_express/commit/f0f5bc8a8f19951da6249aaca9b2dfb8b481b8ae))
* **test:** sort values before checking ([176541f](https://github.com/ssube/prometheus_express/commit/176541fff36be188ad2f691d048ea24a13ce4d5d))
* pc example, deploy script ([5bd18ee](https://github.com/ssube/prometheus_express/commit/5bd18ee52def2f09acb47427d0f3ee3b8b21a7fa))
* **test:** cover registering metrics, utils ([f89c09f](https://github.com/ssube/prometheus_express/commit/f89c09fa2c57cc4a0098ff536a2b9d93fe0850d0))
* rename print methods to render ([a1dcc99](https://github.com/ssube/prometheus_express/commit/a1dcc9990383a0ff2fc33477df29c8ed98ff0360))
* **server:** include error message in settimeout attempt, remove unused params ([30e217f](https://github.com/ssube/prometheus_express/commit/30e217f3621b81df7206646c392536f3adabc26f))
* **server:** refactor into class ([d8caeeb](https://github.com/ssube/prometheus_express/commit/d8caeeb330d72aeb91755383e06b536f18fd7a3c))
