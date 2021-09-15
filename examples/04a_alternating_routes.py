"""
EXAMPLE 04-A: ALTERNATING ROUTES
----------------------------------
TOPIC: Driving, Steering

SETUP: build a nested loop layout

NOTES: This program shows how to alternate steering directions between left
and right. It makes the train alternately go straight and turn on the nested
loop track. This example uses busy-waiting to set the next steering decision
after the previous decision value is used and cleared.
"""
import time

from intelino.trainlib import TrainScanner
from intelino.trainlib.enums import SteeringDecision


def main():
    with TrainScanner() as train:
        start_driving = True
        split_counter = 0

        # infinite loop, so exit with Ctrl + C
        while True:
            # pick a side based on the counter
            if split_counter % 2 == 0:
                side = SteeringDecision.RIGHT
                color = (0, 0, 255)  # blue
            else:
                side = SteeringDecision.LEFT
                color = (255, 0, 0)  # red

            print(f"Next {repr(side)}, splits seen: {split_counter}")
            train.set_next_split_steering_decision(side)
            train.set_headlight_color(color, color)

            if start_driving:
                # start driving after the next decision is set
                train.drive_at_speed(40)
                start_driving = False

            # wait until the `next_split_decision` is cleared
            while train.next_split_decision != SteeringDecision.NONE:
                # check every 10ms
                time.sleep(0.010)

            # a cleared `next_split_decision` means it was used on a split-track
            split_counter += 1


if __name__ == "__main__":
    main()
