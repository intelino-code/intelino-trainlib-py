"""
EXAMPLE 02-A: BLINK TOP LED
---------------------------
TOPIC: LED lights

SETUP: no track needed

NOTES: Blink the top LED on the intelino train 5 times using random colors.
"""
import random
import time
from intelino.trainlib import TrainScanner


def main():
    with TrainScanner() as train:
        blink_delay = 0.5  # in seconds

        for _ in range(5):
            red = random.randint(0, 1) * 255
            green = random.randint(0, 1) * 255
            blue = random.randint(0, 1) * 255

            # turn LED on
            train.set_top_led_color(red, green, blue)
            time.sleep(blink_delay)

            # turn LED off
            train.set_top_led_color(0, 0, 0)
            time.sleep(blink_delay)


if __name__ == "__main__":
    main()
