"""
EXAMPLE 03-A: DRIVING SPEEDS
------------------------------
TOPIC: Driving, Speed Control, Distance

SETUP: build a circle layout using 8 curve tracks and place the train anywhere on it

NOTES: Control the train's driving speed. First, using predefined speed levels,
then with manual speeds in cm/s. Use the circumference of the circle track to
change speed level after each lap, then briefly stop and gradually accelerate
from 20 to 80 cm/s over 3 laps.
"""

import time

from intelino.trainlib import TrainScanner
from intelino.trainlib.enums import (
    MovementDirection,
    SpeedLevel,
    StopDrivingFeedbackType,
)

# Constant: 1 circle track length is approx. 127 cm (PI * 40.5 cm)
CIRCLE_LENGTH_CM = 127.0


def main():
    with TrainScanner() as train:
        #
        # Run 3 loops to test out the 3 predefined speed levels.
        #
        train.drive_at_speed_level(
            # start slow
            speed_level=SpeedLevel.LEVEL1,
            # optional: direction defaults to forward, if not specified
            direction=MovementDirection.FORWARD,
            # optional: whether to blink the top LED, defaults to True
            play_feedback=True,
        )
        # wait until the train drives 1 circle length
        while train.distance_cm < 1 * CIRCLE_LENGTH_CM:
            time.sleep(0.001)  # 1ms sleep

        # medium speed
        train.drive_at_speed_level(SpeedLevel.LEVEL2)
        while train.distance_cm < 2 * CIRCLE_LENGTH_CM:
            time.sleep(0.001)

        # fast
        train.drive_at_speed_level(SpeedLevel.LEVEL3)
        while train.distance_cm < 3 * CIRCLE_LENGTH_CM:
            time.sleep(0.001)

        # stop and rest for a moment
        train.stop_driving(StopDrivingFeedbackType.END_ROUTE)
        time.sleep(3)

        # reset train distance measurement
        train.distance_cm = 0

        #
        # Run 3 loops on a circle while smoothly increasing train speed.
        #
        slow_cmps = 20
        fast_cmps = 80
        step_count = fast_cmps - slow_cmps
        # calculate how long (in cm) we drive at every speed
        step_length_cm = 3 * CIRCLE_LENGTH_CM / step_count

        # start slow
        current_speed_cmps = slow_cmps
        while train.distance_cm < 3 * CIRCLE_LENGTH_CM:
            start_cm = train.distance_cm
            train.drive_at_speed(current_speed_cmps)
            while (train.distance_cm - start_cm) < step_length_cm:
                time.sleep(0.001)  # 1ms sleep

            # increase the speed for the next iteration
            current_speed_cmps += 1

        train.stop_driving(StopDrivingFeedbackType.END_ROUTE)


if __name__ == "__main__":
    main()
