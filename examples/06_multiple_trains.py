"""
EXAMPLE 06: MULTIPLE TRAINS
-----------------------------
TOPIC: Connecting to Multiple Trains, Lights

SETUP: no track needed

NOTES: Easily connect to multiple trains and set their LEDs to the same randomly-picked color.
You can set the `train_count` variable to the number of trains you have availble.
"""
import random
import time
from intelino.trainlib import TrainScanner


def random_rgb_color():
    red = random.randint(0, 1) * 255
    green = random.randint(0, 1) * 255
    blue = random.randint(0, 1) * 255

    return (red, green, blue)


def main():
    train_count = 2
    blink_delay = 0.5  # in seconds

    print("scanning and connecting...")

    trains = TrainScanner(timeout=3.0).get_trains(train_count)

    print("connected train count:", len(trains))

    # set the same random color on all trains
    for _ in range(10):
        color = random_rgb_color()
        for train in trains:
            train.set_top_led_color(*color)
            train.set_headlight_color(front=color, back=color)
        time.sleep(blink_delay)

    print("disconnecting...")

    # cleanup
    for train in trains:
        train.set_top_led_color(0, 0, 0)
        train.set_headlight_color()
        train.disconnect()


if __name__ == "__main__":
    main()
