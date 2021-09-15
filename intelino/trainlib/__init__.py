# Copyright 2021 Innokind, Inc. DBA Intelino
#
# Licensed under the Intelino Public License Agreement, Version 1.0 located at
# https://intelino.com/intelino-public-license.
# BY INSTALLING, DOWNLOADING, ACCESSING, USING OR DISTRIBUTING ANY OF
# THE SOFTWARE, YOU AGREE TO THE TERMS OF SUCH LICENSE AGREEMENT.

"""The ``intelino.trainlib`` package is very similar in function (and API)
to the ``intelino.trainlib_async`` package. They share most of the constants
(via enums), message definitions and also exceptions. In fact, the ``trainlib``
synchronous library is only a wrapper around ``trainlib_async`` executing it
in standard threads, thus allowing synchronous calls to the API.

The only two classes the libraries do not share (and are significantly
different) are :class:`TrainScanner` and :class:`Train`. So only for these
two classes it is important from which package they are imported::

   from intelino.trainlib import TrainScanner, Train

All other classes can be also imported from ``intelino.trainlib_async``.
"""

from .train import Train
from .train_scanner import TrainScanner


__version__ = "1.0.0"
