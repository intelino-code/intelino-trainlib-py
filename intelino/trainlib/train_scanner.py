# Copyright 2021 Innokind, Inc. DBA Intelino
#
# Licensed under the Intelino Public License Agreement, Version 1.0 located at
# https://intelino.com/intelino-public-license.
# BY INSTALLING, DOWNLOADING, ACCESSING, USING OR DISTRIBUTING ANY OF
# THE SOFTWARE, YOU AGREE TO THE TERMS OF SUCH LICENSE AGREEMENT.

"""Simplified train scanning and instantiation."""

import asyncio
from typing import List

from intelino.trainlib_async.train_factory import TrainFactory

from .train import Train
from .exc import TrainNotFoundError


class TrainScanner:
    """Obtaining a :class:`Train` object using the ``with`` statement.

    Connecting to a single train (basic usage)::

        with TrainScanner() as train:
            train.drive_at_speed(40)

    Connecting to multiple trains::

        trains = TrainScanner(timeout=3.0).get_trains(2)
        for train in trains:
            train.drive_at_speed(40)

    """

    def __init__(self, device_identifier: str = None, timeout: float = 5.0):
        """
        Args:
            device_identifier (str): The Bluetooth/UUID address of the Bluetooth
                peripheral sought. If not specified, it will return the first
                found intelino train.
            timeout (float): Optional timeout to wait for detection of specified
                peripheral before giving up. Defaults to 5.0 seconds.
        """
        self.device_identifier = device_identifier
        self.timeout = timeout

    # Synchronous (blocking) Context managers

    def __enter__(self):
        self.blocking_train = self.get_train()
        return self.blocking_train

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.blocking_train.disconnect()

    def get_train(self, **kwargs) -> Train:
        """Get a blocking train instance synchronously.

        Keyword Args:
            adapter (str): Bluetooth adapter to use for discovery.

        Raises:
            TrainNotFoundError: If no train is found.

        Returns:
            A connected :class:`Train` instance.
        """
        train = asyncio.run(
            TrainFactory.create_train(
                device_identifier=kwargs.pop(
                    "device_identifier", self.device_identifier
                ),
                timeout=kwargs.pop("timeout", self.timeout),
                connect=False,
                **kwargs,
            )
        )

        if train is None:
            raise TrainNotFoundError("Train not found!")

        return Train(train)

    def get_trains(self, count: int = None, **kwargs) -> List[Train]:
        """Get a list of blocking train instances synchronously.

        Args:
            count (int): Optional detection limit. If not satisfied, raises an
                exception. If omited or 0, it searches for all trains in
                the surroundings until it timeouts.

        Keyword Args:
            at_most (int): Connect to at most N trains. No exception is raised
                if the `count` argument is omitted.
            adapter (str): Bluetooth adapter to use for discovery.

        Raises:
            TrainNotFoundError: If the requested number of trains is not found.

        Returns:
            A list of :class:`Train` instances.

        Example:
            >>> # connect to all trains in 5 seconds (always takes 5 seconds)
            >>> trains = TrainScanner(timeout=5.0).get_trains()
            >>> # connect to exactly 2 trains, max. waiting time 3 seconds
            >>> trains = TrainScanner(timeout=3.0).get_trains(2)
            >>> # connect to 0 - 4 trains within 10 seconds
            >>> trains = TrainScanner(timeout=10.0).get_trains(at_most=4)

        """
        trains = asyncio.run(
            TrainFactory.create_trains(
                count=kwargs.pop("count", kwargs.pop("at_most", count)),
                timeout=kwargs.pop("timeout", self.timeout),
                connect=False,
                **kwargs,
            )
        )

        if count and (len(trains) != count):
            raise TrainNotFoundError(
                f"Could not find all the requested trains (got {len(trains)} instead of {count})!"
            )

        return list(map(Train, trains))
