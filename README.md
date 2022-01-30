
# intelino-trainlib-py

[![Documentation Status](https://readthedocs.org/projects/intelino-trainlib-py/badge/?version=latest)](https://intelino-trainlib-py.readthedocs.io/en/latest/?badge=latest)
[![PyPI](https://img.shields.io/pypi/v/intelino-trainlib.svg)](https://pypi.org/project/intelino-trainlib/)
[![PyPI](https://img.shields.io/pypi/pyversions/intelino-trainlib.svg)](https://pypi.org/project/intelino-trainlib/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

Python library (SDK) for interacting with the intelino smart train.

![intelino smart trains][main-img]


## Overview

Intelino Smart Train is an award-winning programmable robotic toy that is both fun and educational. Powered by innovative robotic tech, the smart train offers multiple programming modes suitable for users of different ages.

Learning is more meaningful and relatable when experimenting with and simulating real world problems. Younger kids use screen-free activities and tactile coding to operate the smart trains and make them run on schedule. And older users, students and makers use our advanced tools to build smart rail systems and experiment with autonomous driving, collision avoidance, route optimization, resource sharing and much more!

We offer both synchronous and asynchronous Python programming libraries for the intelino smart train. The `intelino-trainlib` is our synchronous Python library. It gives access to our full-featured API, enables event-based programming (through threads) and allows to interactively control one or multiple smart trains. This library is well suited for students and users that are new to Python or text-based programming, in general. And programmers with more advanced skills may prefer our asynchronous library `intelino-trainlib-async` which offers an extended list of API features, Rx-based reactive programming and superior performance.

The code executes in a python interpreter running on your computer - which connects to the train via bluetooth low energy.

## Installation

The intelino trainlib is available on PyPi and can be installed with pip:

```
python3 -m pip install intelino-trainlib
```

## Scanning

```
python3 -m intelino.scan
```


## Local development:

```
git clone git://github.com/intelino-code/intelino-trainlib-py
cd intelino-trainlib-py

python3 -m venv .env
source .env/bin/activate
python3 -m pip install -r requirements.txt
python3 -m pip install -r requirements-dev.txt
python3 -m pip install -e .
```

[main-img]: ./docs/source/images/intelino-multi-train.jpg "intelino smart trains"
