"""
EXAMPLE 03-B: RAINBOW DRIVE
------------------------------
TOPIC: Driving, LED Lights, Distance

SETUP: build any track layout

NOTES: Gradually change the train's top LED color hue based on the distance travelled.
Use the 'colorsys.hsv_to_rgb' function to convert the distance-based color hue to RGB
color space and then scale the values to byte values.
"""
import colorsys
import time
from intelino.trainlib import TrainScanner
from intelino.trainlib.enums import SpeedLevel


def main():
    with TrainScanner() as train:
        # let 1 rainbow be 100 cm
        rainbow_length = 100

        # make sure our rainbow colors are not interrupted by other animations
        train.set_snap_command_feedback(sound=True, lights=False)

        train.drive_at_speed_level(SpeedLevel.LEVEL2)

        # infinite loop, so exit with Ctrl + C
        while True:
            rainbow_position = train.distance_cm % rainbow_length

            # HSV rainbow color
            hsv_coordinate = (rainbow_position / rainbow_length, 1, 1)
            # convert HSV to RGB
            rgb_coordinate = colorsys.hsv_to_rgb(*hsv_coordinate)
            # scale RGB coordinate values (0-1) to bytes (0-255)
            rgb_bytes = tuple(int(255 * val) for val in rgb_coordinate)

            # set LED color
            train.set_top_led_color(*rgb_bytes)

            time.sleep(0.1)


if __name__ == "__main__":
    main()
