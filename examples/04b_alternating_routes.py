"""
EXAMPLE 04-B: ALTERNATING ROUTES
----------------------------------
TOPICS: Driving, Steering, Events

SETUP: build a nested loop layout

NOTES: This example shows another approach to accomplish
alternating steering using the split decision event. Whenever the
split decision event notification is received from the train,
the next steering decision is set based on the value of the
`split_counter` variable being even or odd. The `input` function is
used for convenient program exiting.
"""
from intelino.trainlib import TrainScanner, Train
from intelino.trainlib.enums import SteeringDecision
from intelino.trainlib.messages import TrainMsgEventSplitDecision


def main():
    with TrainScanner() as train:
        split_counter = 0

        def set_decision_and_headlights():
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

        def handle_splits(train: Train, msg: TrainMsgEventSplitDecision):
            nonlocal split_counter
            split_counter += 1
            set_decision_and_headlights()

        set_decision_and_headlights()
        train.add_split_decision_listener(handle_splits)
        train.drive_at_speed(40)

        # block until the user wants to exit
        input("Press the Enter key to exit...\n")

        # cleanup
        train.remove_split_decision_listener(handle_splits)
        train.set_headlight_color()
        train.stop_driving()


if __name__ == "__main__":
    main()
