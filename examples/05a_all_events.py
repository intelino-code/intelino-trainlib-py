"""
EXAMPLE 05-A: ALL EVENTS
---------------------------
TOPIC: Events

SETUP: build any track layout

NOTES: This example gives a basic overview of all events available from
the train. Detected event messages are printed on the screen.
"""
from intelino.trainlib import TrainScanner, Train
from intelino.trainlib.messages import (
    TrainMsgEventBackColorChanged,
    TrainMsgEventButtonPressDetected,
    TrainMsgEventFrontColorChanged,
    TrainMsgEventLowBattery,
    TrainMsgEventMovementDirectionChanged,
    TrainMsgEventSnapCommandDetected,
    TrainMsgEventSnapCommandExecuted,
    TrainMsgEventSplitDecision,
)


def handle_direction_change(train: Train, msg: TrainMsgEventMovementDirectionChanged):
    print("direction changed to:", msg.direction)


def handle_low_battery(train: Train, msg: TrainMsgEventLowBattery):
    print("low battery")


def handle_button_press(train: Train, msg: TrainMsgEventButtonPressDetected):
    print("button press:", msg.button_press_type)


def handle_snap_command_detection(train: Train, msg: TrainMsgEventSnapCommandDetected):
    print("snap command detected:", msg.colors)


def handle_snap_command_execution(train: Train, msg: TrainMsgEventSnapCommandExecuted):
    print("snap command executed:", msg.colors)


def handle_front_color_change(train: Train, msg: TrainMsgEventFrontColorChanged):
    print("front sensor color:", msg.color)


def handle_back_color_change(train: Train, msg: TrainMsgEventBackColorChanged):
    print("back sensor color:", msg.color)


def handle_split_decision(train: Train, msg: TrainMsgEventSplitDecision):
    print("split decision made, the train went:", msg.decision)


def main():
    with TrainScanner() as train:
        train.add_movement_direction_change_listener(handle_direction_change)
        train.add_low_battery_listener(handle_low_battery)
        train.add_button_press_listener(handle_button_press)
        train.add_snap_command_detection_listener(handle_snap_command_detection)
        train.add_snap_command_execution_listener(handle_snap_command_execution)
        train.add_front_color_change_listener(handle_front_color_change)
        train.add_back_color_change_listener(handle_back_color_change)
        train.add_split_decision_listener(handle_split_decision)

        print("Try running the train and observe the event stream.")
        input("When done, press Enter to exit...\n")

        train.remove_movement_direction_change_listener(handle_direction_change)
        train.remove_low_battery_listener(handle_low_battery)
        train.remove_button_press_listener(handle_button_press)
        train.remove_snap_command_detection_listener(handle_snap_command_detection)
        train.remove_snap_command_execution_listener(handle_snap_command_execution)
        train.remove_front_color_change_listener(handle_front_color_change)
        train.remove_back_color_change_listener(handle_back_color_change)
        train.remove_split_decision_listener(handle_split_decision)


if __name__ == "__main__":
    main()
