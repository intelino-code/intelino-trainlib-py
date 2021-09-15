"""
EXAMPLE 07: SIMPLE COLLISION AVOIDANCE
-----------------------------------------
TOPIC: Multiple Trains, Driving, Steering, Snap Command and Color Events

SETUP: build a nested loop track with a shared track section

NOTES: This example demonstrates a simple solution for a 2-train merge or head-on collision
avoidance on a shared track section (referred to as 'pass' in this program). For head-on 
collsion avoidance, one of the trains needs to move clockwise and the other counter-clockwise.
Also, you can use default steering snap commands to make the trains run separate routes and only
share the 'pass' section.

Based on the movement direction of each train, place WHITE-MAGENTA snap
commands prior to the entrance to the 'pass' on both sides of the shared section. 
Similarly, place YELLOW snaps after the 'pass' section. 

The WHITE-MAGENTA snap command's handling function acts as a "traffic light", which
either lets a train pass or stops it until the section is 'freed' by the other train 
when it passes over the YELLOW snap.
"""
import time
from intelino.trainlib import TrainScanner, Train
from intelino.trainlib.enums import SnapColorValue as C
from intelino.trainlib.messages import (
    TrainMsgEventFrontColorChanged,
    TrainMsgEventSnapCommandDetected,
)


def main():
    trains = TrainScanner().get_trains(count=3)
    # shared variable that represents the state of the pass
    pass_used_by = None

    def enter_pass(train: Train):
        nonlocal pass_used_by
        if pass_used_by is None:
            pass_used_by = train.id
            print(train.alias, "entered the pass")

        else:
            train.stop_driving()
            print(train.alias, "waits for the pass to be free")
            while pass_used_by is not None:
                time.sleep(0.010)  # busy wait, check every 10ms
            pass_used_by = train.id
            train.drive_at_speed(40)
            print(train.alias, "entered the pass (after waiting)")

    def leave_pass(train: Train):
        nonlocal pass_used_by
        if pass_used_by == train.id:
            pass_used_by = None
            print(train.alias, "left the pass")

    def handle_snap_commands(train: Train, msg: TrainMsgEventSnapCommandDetected):
        if msg.colors == (C.WHITE, C.MAGENTA, C.BLACK, C.BLACK):
            enter_pass(train)

    def handle_colors(train: Train, msg: TrainMsgEventFrontColorChanged):
        if msg.color == C.YELLOW:
            leave_pass(train)

    # identify our trains
    trains[0].alias = "Red Train"
    trains[0].set_headlight_color(front=(255, 0, 0), back=(255, 0, 0))
    trains[1].alias = "Blue Train"
    trains[1].set_headlight_color(front=(0, 0, 255), back=(0, 0, 255))

    # setup event listeners
    for train in trains:
        train.clear_custom_snap_commands()
        train.add_snap_command_detection_listener(handle_snap_commands)
        train.add_front_color_change_listener(handle_colors)

    # start driving
    for train in trains:
        train.drive_at_speed(40)

    input("When done, press Enter to exit...\n")

    # cleanup
    for train in trains:
        train.stop_driving()
        train.set_headlight_color()
        train.remove_snap_command_detection_listener(handle_snap_commands)
        train.remove_front_color_change_listener(handle_colors)
        train.disconnect()


if __name__ == "__main__":
    main()
