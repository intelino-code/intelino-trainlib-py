"""
EXAMPLE 05-B: SNAP COMMANDS
-----------------------------
TOPIC: Color Snap Commands, Events

SETUP: build any loop track and add WHITE-RED, WHITE-GREEN and WHITE-BLUE snap commands

NOTES: This example shows how to disable the default snap command actions and 
define custom behaviors. Snap command detection event notifications are used to trigger
the custom actions. In this case, we simply update the top LED color based 
on the second color of each detected snap command.
"""

from intelino.trainlib import TrainScanner, Train
from intelino.trainlib.enums import (
    MovementDirection,
    SnapColorValue as C,
    SpeedLevel,
)
from intelino.trainlib.messages import TrainMsgEventSnapCommandDetected


def handle_snap_commands(train: Train, msg: TrainMsgEventSnapCommandDetected):
    # Note: the `SnapColorValue` enum is imported as `C` for a shorter notation

    if msg.colors == (C.WHITE, C.RED, C.BLACK, C.BLACK):
        # exact match (the missing snaps are detected as black to length 4)
        train.set_top_led_color(r=255, g=0, b=0)

    elif msg.colors == (C.WHITE, C.GREEN):
        # exact match with implicit blacks
        train.set_top_led_color(r=0, g=255, b=0)

    elif msg.colors.start_with(C.WHITE, C.BLUE):
        # partial / prefix match
        train.set_top_led_color(r=0, g=0, b=255)


def main():
    with TrainScanner() as train:
        # disable all snap commands
        # - built in snaps including split track snaps (so no random steering)
        # - custom snaps (starting with white-magenta)
        train.set_snap_command_execution(False)
        train.add_snap_command_detection_listener(handle_snap_commands)

        train.drive_at_speed_level(
            SpeedLevel.LEVEL2, MovementDirection.FORWARD, play_feedback=False
        )

        input("When done, press Enter to exit...\n")

        # cleanup
        train.stop_driving()
        train.remove_snap_command_detection_listener(handle_snap_commands)
        train.set_snap_command_execution(True)


if __name__ == "__main__":
    main()
