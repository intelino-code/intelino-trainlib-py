"""
EXAMPLE 05-C: COLOR DETECTION
-------------------------------
TOPIC: Color Detection, Events

SETUP: build any loop track and add GREEN, YELLOW and MAGENTA individual snaps
around the track

NOTES: In this example, the top LED color is set based on GREEN, YELLOW and MAGENTA
snap detection. We use the color change event notifications to update the LED color.
"""
from intelino.trainlib import TrainScanner, Train
from intelino.trainlib.enums import (
    MovementDirection,
    SnapColorValue as C,
    SpeedLevel,
)
from intelino.trainlib.messages import TrainMsgEventSensorColorChanged


def handle_color_change(train: Train, msg: TrainMsgEventSensorColorChanged):
    # Note: the `SnapColorValue` enum is imported as `C` for a shorter notation

    # Note: we picked green, yellow, and magenta, because these colors are not
    # used on split tracks. Split tracks have embedded cyan, red, and blue
    # colors.

    if msg.color == C.GREEN:
        train.set_top_led_color(r=0, g=255, b=0)

    elif msg.color == C.YELLOW:
        train.set_top_led_color(r=255, g=255, b=0)

    elif msg.color == C.MAGENTA:
        train.set_top_led_color(r=255, g=0, b=255)


def main():
    with TrainScanner() as train:
        # snap command execution can stay on, we only disable LED feedback
        train.set_snap_command_feedback(sound=True, lights=False)

        train.add_front_color_change_listener(handle_color_change)

        train.drive_at_speed_level(
            SpeedLevel.LEVEL2, MovementDirection.FORWARD, play_feedback=False
        )

        input("When done, press Enter to exit...\n")

        # cleanup
        train.remove_front_color_change_listener(handle_color_change)
        train.set_snap_command_feedback(sound=True, lights=True)
        train.stop_driving()


if __name__ == "__main__":
    main()
