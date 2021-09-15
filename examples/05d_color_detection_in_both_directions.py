"""
EXAMPLE 05-D: COLOR DETECTION IN BOTH DIRECTIONS
---------------------------------------------------
TOPIC: Color Detection, Movement Direction, Events

SETUP: build any loop track and add a WHITE-BLUE snap command as well as individual 
snaps in colors GREEN, YELLOW and MAGENTA around the track

NOTES: Similarly to example 05-C, the top LED color is set based on GREEN, YELLOW and 
MAGENTA snap detection. But now the train executes this task in both driving directions.
The leading color sensor is set to front or back based on train's movement direction.  
"""
from intelino.trainlib import TrainScanner, Train
from intelino.trainlib.enums import (
    ColorSensor,
    MovementDirection,
    SnapColorValue as C,
    SpeedLevel,
)
from intelino.trainlib.messages import TrainMsgEventSensorColorChanged


def is_relative_front_sensor(direction: MovementDirection, sensor: ColorSensor) -> bool:
    """Check if the given sensor is a front sensor relative to the movement direction.

    Use back sensor only if really going backwards, use front sensor in all
    other cases (e.g. going forward or stopped - moved by hand)
    """
    accept_sensor = ColorSensor.FRONT
    if direction == MovementDirection.BACKWARD:
        accept_sensor = ColorSensor.BACK

    return sensor == accept_sensor


def handle_color_change(train: Train, msg: TrainMsgEventSensorColorChanged):
    # Note, that we use the `TrainMsgEventSensorColorChanged` union type, so we
    # can assign this callback to both color sensor events.

    if not is_relative_front_sensor(train.direction, msg.sensor):
        # don't handle this sensor event (return early)
        return

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

        # listen to events on both color sensors
        train.add_front_color_change_listener(handle_color_change)
        train.add_back_color_change_listener(handle_color_change)

        train.drive_at_speed_level(
            SpeedLevel.LEVEL2, MovementDirection.FORWARD, play_feedback=False
        )

        input("When done, press Enter to exit...\n")

        # cleanup
        train.remove_front_color_change_listener(handle_color_change)
        train.remove_back_color_change_listener(handle_color_change)
        train.set_snap_command_feedback(sound=True, lights=True)
        train.stop_driving()


if __name__ == "__main__":
    main()
