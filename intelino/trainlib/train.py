# Copyright 2021 Innokind, Inc. DBA Intelino
#
# Licensed under the Intelino Public License Agreement, Version 1.0 located at
# https://intelino.com/intelino-public-license.
# BY INSTALLING, DOWNLOADING, ACCESSING, USING OR DISTRIBUTING ANY OF
# THE SOFTWARE, YOU AGREE TO THE TERMS OF SUCH LICENSE AGREEMENT.

"""Synchronous (blocking) train class."""

import asyncio
from collections import defaultdict
import threading
from typing import Any, Callable, Coroutine, Iterable, List, TypeVar, Union, get_args
from rx import operators as ops
from rx.core.typing import Disposable

from intelino.trainlib_async import Train as AsyncTrain

from .enums import (
    MovementDirection,
    SteeringDecision,
    SpeedLevel,
    StopDrivingFeedbackType,
)
from .messages import (
    EventId,
    TrainMsg,
    TrainMsgEvent,
    TrainMsgEventBackColorChanged,
    TrainMsgEventButtonPressDetected,
    TrainMsgEventFrontColorChanged,
    TrainMsgEventLowBattery,
    TrainMsgEventMovementDirectionChanged,
    TrainMsgEventSnapCommandDetected,
    TrainMsgEventSnapCommandExecuted,
    TrainMsgEventSplitDecision,
    TrainMsgMovement,
)


T = TypeVar("T")


class Train:
    """Synchronous (blocking) version of the intelino train class."""

    def __init__(self, train: AsyncTrain):
        self.__train = train

        self.__event_loop = asyncio.new_event_loop()
        self.__lock = threading.Lock()
        self.__thread = threading.Thread(target=self.__event_loop.run_forever)
        self.__thread.start()

        # buffered values received from the train asynchronously
        self.__odometer_offset = 0
        self.__odometer_last = 0
        self.__direction = MovementDirection.STOP
        self.__speed_cmps = 0
        self.__next_split_decision = SteeringDecision.NONE

        # rx subscriptions
        self.__subscriptions: List[Disposable] = []
        # user listeners
        self.__listeners: dict[EventId, dict[Callable, Callable]] = defaultdict(dict)

        # connect and setup the train
        self.__execute(self.__setup())

    async def __setup(self):
        await self.__train.connect()

        msg = await self.__train.get_movement_notification()
        self.__odometer_offset = msg.lifetime_odometer_meters
        self.__odometer_last = msg.lifetime_odometer_meters
        self.__direction = msg.direction
        self.__speed_cmps = msg.speed_cmps
        self.__next_split_decision = msg.next_split_decision

        movement_stream = await self.__train.movement_notification_stream()

        def sync_local_state(msg: TrainMsgMovement):
            self.__odometer_last = msg.lifetime_odometer_meters
            self.__direction = msg.direction
            self.__speed_cmps = msg.speed_cmps
            self.__next_split_decision = msg.next_split_decision

        self.__subscriptions.append(movement_stream.subscribe(sync_local_state))

        event_stream = self.__train.notifications.pipe(
            # we are interested only in events
            ops.filter(lambda msg: isinstance(msg, get_args(TrainMsgEvent)))
        )

        def handle_event_listeners(msg: TrainMsgEvent):
            for func in self.__listeners[msg.event_id].values():
                # NOTE: consider using a thread pool to improve performance
                threading.Thread(target=func, args=(self, msg)).start()

        self.__subscriptions.append(event_stream.subscribe(handle_event_listeners))

    def __execute(self, coroutine: Coroutine[Any, Any, T], timeout: float = None) -> T:
        with self.__lock:
            return asyncio.run_coroutine_threadsafe(
                coroutine, self.__event_loop
            ).result(timeout)

    def _add_listener(self, event_id: EventId, listener: Callable):
        self.__listeners[event_id][listener] = listener

    def _remove_listener(self, event_id: EventId, listener: Callable):
        self.__listeners[event_id].pop(listener)

    def disconnect(self):
        """Disconnects from the train and cleans up all resources.

        Reconnection of the same blocking train instance is not possible. Create
        a new instance.
        """
        for subscription in self.__subscriptions:
            subscription.dispose()
        self.__execute(self.__train.disconnect())

        with self.__lock:
            self.__event_loop.call_soon_threadsafe(self.__event_loop.stop)
            self.__thread.join()
        self.__event_loop.close()

    @property
    def id(self) -> str:
        """Connection ID / address."""
        return self.__train.id

    @property
    def name(self) -> str:
        """Advertised name."""
        return self.__train.name

    @property
    def alias(self) -> str:
        """User-defined nickname (train alias)."""
        return self.__train.alias

    @alias.setter
    def alias(self, value: str) -> None:
        self.__train.alias = value

    @property
    def is_connected(self) -> bool:
        return self.__train.is_connected

    @property
    def distance_cm(self) -> int:
        return int((self.__odometer_last - self.__odometer_offset) * 100)

    @distance_cm.setter
    def distance_cm(self, value: int) -> None:
        self.__odometer_offset = self.__odometer_last - (value / 100)

    @property
    def direction(self) -> MovementDirection:
        return self.__direction

    @property
    def speed_cmps(self) -> float:
        return self.__speed_cmps

    @property
    def next_split_decision(self) -> SteeringDecision:
        return self.__next_split_decision

    def send_command(self, command_id: int, payload: Iterable[int] = None) -> None:
        return self.__execute(self.__train.send_command(command_id, payload))

    def send_command_with_response(
        self, command_id: int, payload: Iterable[int] = None, timeout: float = 3.0
    ) -> TrainMsg:
        return self.__execute(
            self.__train.send_command_with_response(command_id, payload, timeout)
        ).msg

    def drive_at_speed(
        self,
        speed_cmps: Union[int, float],
        direction: MovementDirection = MovementDirection.FORWARD,
        play_feedback: bool = True,
    ) -> None:
        """Drive with speed control at the given speed in cm/s.

        Args:
            speed_cmps: Desired speed in cm/s. Possible (drivable) values are
                15-75 cm/s. Note: The increment step is 0.9425 cm, so the final
                desired speed might get adjusted by the train.
            direction: Movement direction forward, backward, stop etc.
            play_feedback: Sound and lights.
        """
        return self.__execute(
            self.__train.drive_at_speed(speed_cmps, direction, play_feedback)
        )

    def drive_at_speed_level(
        self,
        speed_level: SpeedLevel,
        direction: MovementDirection = MovementDirection.FORWARD,
        play_feedback: bool = True,
    ) -> None:
        """Start driving at a speed level defined by the train (and green snaps).

        Args:
            speed_level: 1, 2, 3.
            direction: Movement direction forward, backward, stop etc.
            play_feedback: Sound and lights.
        """
        return self.__execute(
            self.__train.drive_at_speed_level(speed_level, direction, play_feedback)
        )

    def stop_driving(
        self,
        play_feedback_type: StopDrivingFeedbackType = StopDrivingFeedbackType.MOVEMENT_STOP,
    ):
        """Stop the train.

        Args:
            play_feedback_type: Sound and lights.
        """
        return self.__execute(self.__train.stop_driving(play_feedback_type))

    def set_next_split_steering_decision(self, next_decision: SteeringDecision) -> None:
        """This steering decision is valid for the next split (detected by it’s snaps).

        It overrides the snap value (if set) or the random choice.

        Args:
            next: The next decision.
        """

        async def helper():
            await self.__train.set_next_split_steering_decision(next_decision)
            # wait for the local state to be updated
            await self.__train.get_movement_notification()
            await asyncio.sleep(0)

        self.__execute(helper())

    def set_top_led_color(self, r: int, g: int, b: int) -> None:
        """Set the top RGB LED color.

        Args:
            r (int): 8bit RGB value for red.
            g (int): 8bit RGB value for green.
            b (int): 8bit RGB value for blue.
        """
        return self.__execute(self.__train.set_top_led_color(r, g, b))

    def set_headlight_color(
        self, front: Iterable[int] = None, back: Iterable[int] = None
    ):
        """Set front and back headlight color (for driving). They switch based
            on movement direction. To reset colors call without parameters.

        Args:
            front: Front 8bit RGB value array [red, green, blue].
            back: Back 8bit RGB value array [red, green, blue].
        """
        return self.__execute(self.__train.set_headlight_color(front, back))

    def set_snap_command_feedback(self, sound: bool, lights: bool):
        """Set snap command behavior feedback.

        Args:
            sound (bool): Sounds on/off.
            lights (bool): Blink top LED on/off.
        """
        return self.__execute(
            self.__train.set_snap_command_feedback(sound, lights)
        )

    def set_snap_command_execution(self, on: bool):
        """Enable or disable snap command execution on the train (from BLE API v1.2).

        Args:
            on (bool): Snap command execution on/off.
        """
        return self.__execute(self.__train.set_snap_command_execution(on))

    def clear_custom_snap_commands(self):
        """Clear user defined custom snap commands stored in the train to avoid
        collisions in behavior in case we would listen and react to these
        events.
        """
        return self.__execute(self.__train.clear_custom_snap_commands())

    def decouple_wagon(self, play_feedback: bool = True):
        """Decouple wagon.

        Args:
            play_feedback: Sound and lights.
        """

        async def helper():
            await self.__train.decouple_wagon(play_feedback)
            await asyncio.sleep(1.5)

        return self.__execute(helper())

    def add_movement_direction_change_listener(
        self, listener: Callable[["Train", TrainMsgEventMovementDirectionChanged], None]
    ):
        self._add_listener(EventId.MOVEMENT_DIRECTION_CHANGED, listener)

    def remove_movement_direction_change_listener(
        self, listener: Callable[["Train", TrainMsgEventMovementDirectionChanged], None]
    ):
        self._remove_listener(EventId.MOVEMENT_DIRECTION_CHANGED, listener)

    def add_low_battery_listener(
        self, listener: Callable[["Train", TrainMsgEventLowBattery], None]
    ):
        self._add_listener(EventId.LOW_BATTERY, listener)

    def remove_low_battery_listener(
        self, listener: Callable[["Train", TrainMsgEventLowBattery], None]
    ):
        self._remove_listener(EventId.LOW_BATTERY, listener)

    def add_button_press_listener(
        self, listener: Callable[["Train", TrainMsgEventButtonPressDetected], None]
    ):
        self._add_listener(EventId.BUTTON_PRESS_DETECTED, listener)

    def remove_button_press_listener(
        self, listener: Callable[["Train", TrainMsgEventButtonPressDetected], None]
    ):
        self._remove_listener(EventId.BUTTON_PRESS_DETECTED, listener)

    def add_snap_command_detection_listener(
        self, listener: Callable[["Train", TrainMsgEventSnapCommandDetected], None]
    ):
        self._add_listener(EventId.SNAP_COMMAND_DETECTED, listener)

    def remove_snap_command_detection_listener(
        self, listener: Callable[["Train", TrainMsgEventSnapCommandDetected], None]
    ):
        self._remove_listener(EventId.SNAP_COMMAND_DETECTED, listener)

    def add_snap_command_execution_listener(
        self, listener: Callable[["Train", TrainMsgEventSnapCommandExecuted], None]
    ):
        self._add_listener(EventId.SNAP_COMMAND_EXECUTED, listener)

    def remove_snap_command_execution_listener(
        self, listener: Callable[["Train", TrainMsgEventSnapCommandExecuted], None]
    ):
        self._remove_listener(EventId.SNAP_COMMAND_EXECUTED, listener)

    def add_front_color_change_listener(
        self, listener: Callable[["Train", TrainMsgEventFrontColorChanged], None]
    ):
        self._add_listener(EventId.FRONT_COLOR_CHANGED, listener)

    def remove_front_color_change_listener(
        self, listener: Callable[["Train", TrainMsgEventFrontColorChanged], None]
    ):
        self._remove_listener(EventId.FRONT_COLOR_CHANGED, listener)

    def add_back_color_change_listener(
        self, listener: Callable[["Train", TrainMsgEventBackColorChanged], None]
    ):
        self._add_listener(EventId.BACK_COLOR_CHANGED, listener)

    def remove_back_color_change_listener(
        self, listener: Callable[["Train", TrainMsgEventBackColorChanged], None]
    ):
        self._remove_listener(EventId.BACK_COLOR_CHANGED, listener)

    def add_split_decision_listener(
        self, listener: Callable[["Train", TrainMsgEventSplitDecision], None]
    ):
        self._add_listener(EventId.SPLIT_DECISION, listener)

    def remove_split_decision_listener(
        self, listener: Callable[["Train", TrainMsgEventSplitDecision], None]
    ):
        self._remove_listener(EventId.SPLIT_DECISION, listener)
