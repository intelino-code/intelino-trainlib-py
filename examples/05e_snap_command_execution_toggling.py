"""
EXAMPLE 05-E: SNAP COMMAND EXECUTION TOGGLING
------------------------------------------------
TOPIC: Snap Command Detection, Color Detection, Lights, Events

SETUP: build any loop track and add two separate WHITE-GREEN snap commands and a YELLOW
individual snap around the track

NOTES: In this example, the train toggles between the default and custom behaviors
when it detects the WHITE-GREEN snap command. When the default behavior execution is
disabled, the train stops for 2 seconds while all LEDs turn RED. When the default behavior
is enabled, the WHITE-GREEN snap command is executed with the normal behavior AND with
all LEDs set to GREEN. The YELLOW snap command detection is used for updating the LEDs
to YELLOW and disabling the snap command execution.
"""
import time
from intelino.trainlib import TrainScanner, Train
from intelino.trainlib.enums import StopDrivingFeedbackType
from intelino.trainlib.enums import SnapColorValue as C
from intelino.trainlib.messages import (
    TrainMsgEventFrontColorChanged,
    TrainMsgEventSnapCommandDetected,
)


def main():
    with TrainScanner() as train:

        # disable default snap commands and feedback effects
        train.set_snap_command_execution(False)
        train.set_snap_command_feedback(sound=True, lights=False)
        color_commands = False

        # define snap command actions
        def handle_snap_commands(train: Train, msg: TrainMsgEventSnapCommandDetected):
            nonlocal color_commands

            # define actions for WHITE GREEN snap sequence
            if msg.colors == (C.WHITE, C.GREEN, C.BLACK, C.BLACK):

                # custom behavoir when default commands are disabled
                if color_commands is False:
                    train.set_top_led_color(255, 0, 0)
                    train.set_headlight_color(front=(255, 0, 0), back=(255, 0, 0))
                    train.stop_driving(play_feedback_type=StopDrivingFeedbackType.NONE)
                    time.sleep(2.0)
                    train.set_snap_command_execution(True)
                    train.set_top_led_color(0, 255, 255)
                    train.set_headlight_color()
                    train.drive_at_speed(40)
                    color_commands = True

                # only turn on LEDs to green when default commands are enabled
                else:
                    train.set_top_led_color(0, 255, 0)
                    train.set_headlight_color(front=(0, 255, 0), back=(0, 255, 0))

        # define actions when color yellow is detected
        def handle_colors(train: Train, msg: TrainMsgEventFrontColorChanged):
            nonlocal color_commands
            if msg.color == C.YELLOW:
                train.set_top_led_color(255, 255, 0)
                train.set_headlight_color(front=(255, 255, 0), back=(255, 255, 0))
                train.set_snap_command_execution(False)
                train.drive_at_speed(40)
                color_commands = False

        # setup event listeners
        train.add_snap_command_detection_listener(handle_snap_commands)
        train.add_front_color_change_listener(handle_colors)

        # set top LED to cyan and start driving forward at 40 cm/s
        train.set_top_led_color(0, 255, 255)
        print("Start driving forward")
        train.drive_at_speed(40)

        input("When done, press Enter to exit...\n")

        # cleanup
        train.stop_driving()
        train.set_top_led_color(0, 0, 0)
        train.set_headlight_color()
        train.remove_snap_command_detection_listener(handle_snap_commands)
        train.remove_front_color_change_listener(handle_colors)


if __name__ == "__main__":
    main()
