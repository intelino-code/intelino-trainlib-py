"""
EXAMPLE 02-B: LIGHTS
---------------------------
TOPIC: LED lights

SETUP: no track needed

NOTES: Sequentially set train's top, front and rear LED lights to red, green and blue.
"""
import time
from intelino.trainlib import TrainScanner


def main():
    with TrainScanner() as train:
        color_change_delay = 2.0  # in seconds

        rgb_red = (255, 0, 0)
        rgb_green = (0, 255, 0)
        rgb_blue = (0, 0, 255)
        rgb_black = (0, 0, 0)

        # red
        train.set_top_led_color(*rgb_red)
        train.set_headlight_color(rgb_red, rgb_red)
        time.sleep(color_change_delay)

        # green
        train.set_top_led_color(*rgb_green)
        train.set_headlight_color(rgb_green, rgb_green)
        time.sleep(color_change_delay)

        # blue
        train.set_top_led_color(*rgb_blue)
        train.set_headlight_color(rgb_blue, rgb_blue)
        time.sleep(color_change_delay)

        # turn top LED off
        train.set_top_led_color(*rgb_black)
        # reset headlights and taillights
        train.set_headlight_color()


if __name__ == "__main__":
    main()
