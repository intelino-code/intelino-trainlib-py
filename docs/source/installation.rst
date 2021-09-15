Library Installation
=====================

Global Installation
--------------------

The **intelino trainlib** library is available on PyPi and can be installed globally on your system with `pip`_:

.. code-block:: console

   $ python3 -m pip install intelino-trainlib

Project page on PyPi: https://pypi.org/project/intelino-trainlib

This is the preferred installation method for **intelino trainlib**, and it will always
install the latest stable release of the library.

Local Environment Installation
--------------------------------

If you prefer to do a local environment installation of this library, follow the steps described below.

First, create a new directory/folder where you'd like to install the library. Then navigate to this directory in the terminal and run the following commands to setup the library environment, activate it and install the library:

.. code-block:: console

   $ python3 -m venv .env
   $ source .env/bin/activate
   $ python3 -m pip install intelino-trainlib

Note that when using a locally-installed library, you will always need to first go to the library's root directory and activate the environment by running ``source .env/bin/activate`` (whenever you open a new terminal window) for the library to work.

Requirements and Dependencies
-----------------------------

This library is supported on machines running Windows 10, macOS and Linux operating systems equipped with Bluetooth 4.0 or greater.

.. note:: **intelino trainlib** requires Python 3.7 (or higher) and
          ``pip`` package-management system

If you have an older version of Python or don't have `pip`_ on your system, you may see errors while installing the library on your machine. To resolve the baseline setup issues and install the required software packages, refer to this `Python installation guide`_ which will guide you through the process. Then try installing the **intelino trainlib** library again.

.. _pip: https://pip.pypa.io
.. _Python installation guide: http://docs.python-guide.org/en/latest/starting/installation/

This synchronous (blocking) library variant of `trainlib` depends directly on its asynchronous sibling ``intelino-trainlib-async`` which will be installed automatically. The ``intelino-trainlib-async`` library  has the following external library dependencies (also installed automatically by ``pip``):

* Bleak library
   * `"Bleak is an acronym for Bluetooth Low Energy platform Agnostic Klient."`
      * Supports Windows 10, version 16299 (Fall Creators Update) or greater
      * Supports Linux distributions with BlueZ >= 5.43
      * OS X/macOS support via Core Bluetooth API, from at least OS X version 10.11
   * homepage: https://github.com/hbldh/bleak
   * docs: https://bleak.readthedocs.io/

* ReactiveX (Rx) library
   * `"ReactiveX is a library for composing asynchronous and event-based programs by using observable sequences."`
      * OS independent
   * homepage: http://reactivex.io/
   * git repo: https://github.com/ReactiveX/RxPY
   * docs: https://rxpy.readthedocs.io/

Local Development and Testing
-------------------------------

For local development and testing, clone the library repository and setup your environment:

.. code-block:: console

   $ git clone git://github.com/intelino-code/intelino-trainlib-py
   $ cd intelino-trainlib-py

   $ python3 -m venv .env
   $ source .env/bin/activate
   $ python3 -m pip install -r requirements.txt
   $ python3 -m pip install -r requirements-dev.txt
   $ python3 -m pip install -e .
