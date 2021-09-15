"""
EXAMPLE 08: WAGON EXCHANGE
---------------------------
TOPIC: Multiple Trains, Driving, Steering, Wagon Decoupling, Snap Command Events

SETUP: build a track with nested loops on both sides (using 4x splits, 2x straights, 12x curves).
Add snap commands as follows:
    - WHITE-MAGENTA-WHITE: double sided snap command for wagon drop off and pickup
      on both inner loop sides
    - WHITE-MAGENTA-RED: waiting state on the outer loops on both sides
    - WHITE-MAGENTA-BLUE: reversing maneuver for wagon pickup
      between the split tracks (on a straight segment)
The trains should start on the outer loops opposite from each other

NOTES: This example enables wagon exchange between two trains. The WHITE-MAGENTA-WHITE
snap commands are used to 'mark' the wagon drop off areas on the track. Each train
delivers the wagon and moves to the waiting area of the track marked with WHITE-MAGENTA-RED.
The moment the drop-off occurs, the other train receives a notification to proceed to the
wagon pick-up.
"""
import collections
from enum import Enum
import random
from typing import Callable, NamedTuple
from intelino.trainlib import TrainScanner, Train
from intelino.trainlib.enums import (
    SnapColorValue as Color,
    MovementDirection,
    SteeringDecision,
)
from intelino.trainlib.messages import TrainMsgEventSnapCommandDetected

#
# Data types
#

WagonState = Enum("WagonState", "UNKNOWN CARRIED_BY READY_FOR")


class WagonInfo(NamedTuple):
    state: WagonState
    train_alias: str


class TrainState:
    def __init__(self):
        # waiting for the wagon to be ready for us
        self.waiting = True
        # when carrying the wagon, we need to pass a checkpoint before drop off
        # is allowed
        self.checkpoint_passed = False


class SharedState:
    def __init__(self):
        self.wagon = WagonInfo(WagonState.UNKNOWN, "")
        # train state indexed by the train's alias
        self.trains: dict[str, TrainState] = collections.defaultdict(TrainState)


#
# Functions
#


def train_setup_function(
    train: Train, state: SharedState, wagon_ready_notifier: Callable
):
    # snap command handler callback
    def milestone(train: Train, msg: TrainMsgEventSnapCommandDetected):
        # for easier readability, saving our alias as "me"
        me = train.alias

        if msg.colors == (Color.WHITE, Color.MAGENTA, Color.BLACK, Color.BLACK):
            # inner loop - wagon exchange place
            if (state.wagon == (WagonState.CARRIED_BY, me)) and state.trains[
                me
            ].checkpoint_passed:
                # drop off (and make sure to update the state asap)
                state.wagon = WagonInfo(WagonState.READY_FOR, "")
                train.decouple_wagon()
                print(me, "wagon dropped off")
                # navigate home
                train.set_next_split_steering_decision(SteeringDecision.STRAIGHT)
                # pick a next train to have the wagon
                train_aliases = list(state.trains.keys())
                train_aliases.remove(me)
                next_train = random.choice(train_aliases)
                state.wagon = WagonInfo(WagonState.READY_FOR, next_train)
                # inform the other train of the wagon being ready
                wagon_ready_notifier()

            elif state.wagon == (WagonState.READY_FOR, me):
                # pickup
                # "hope" that we attached the wagon
                state.trains[me].checkpoint_passed = False
                train.drive_at_speed(40, MovementDirection.FORWARD)
                train.set_next_split_steering_decision(SteeringDecision.LEFT)
                state.wagon = WagonInfo(WagonState.CARRIED_BY, me)
                print(me, "wagon picked up")

        elif msg.colors.start_with(Color.WHITE, Color.MAGENTA, Color.RED):
            # outer loop - resting place
            if state.wagon.train_alias != me:
                # wagon is not ours (nor carried by nor ready for us)
                state.trains[me].waiting = True
                train.stop_driving()
                print(me, "waiting")

        elif msg.colors.start_with(Color.WHITE, Color.MAGENTA, Color.BLUE):
            # middle section - checkpoint
            if state.wagon == (WagonState.CARRIED_BY, me):
                state.trains[me].checkpoint_passed = True
                train.set_next_split_steering_decision(SteeringDecision.LEFT)
                print(me, "reached checkpoint with a wagon")

            elif state.wagon == (WagonState.READY_FOR, me):
                # reverse for pickup
                train.drive_at_speed(30, MovementDirection.BACKWARD)
                train.set_next_split_steering_decision(SteeringDecision.RIGHT)

    # clear all custom snap commands stored on the train (just to be sure)
    train.clear_custom_snap_commands()
    # disable built-in snap commands (just to be sure)
    train.set_snap_command_execution(False)
    # register the "milestone" listener
    train.add_snap_command_detection_listener(milestone)


def main():
    print("Connecting...")
    trains = TrainScanner().get_trains(count=2)

    # identify our trains
    trains[0].alias = "Red Train"
    trains[0].set_headlight_color(front=(255, 0, 0), back=(255, 0, 0))
    trains[1].alias = "Blue Train"
    trains[1].set_headlight_color(front=(0, 0, 255), back=(0, 0, 255))

    # the "first" train to have the wagon should glow green
    trains[0].set_top_led_color(0, 255, 0)
    input("Attach the wagon to the train with a green top LED and press Enter...\n")

    # initialize the state
    shared_state = SharedState()
    shared_state.wagon = WagonInfo(WagonState.CARRIED_BY, trains[0].alias)
    for train in trains:
        # all trains are waiting
        shared_state.trains[train.alias].waiting = True
    # except the first one
    shared_state.trains[trains[0].alias].waiting = False

    def handle_wagon_ready():
        if shared_state.wagon.state == WagonState.READY_FOR:
            alias = shared_state.wagon.train_alias
            if shared_state.trains[alias].waiting:
                # search for the train and "wake up"
                for train in trains:
                    if train.alias == alias:
                        train.drive_at_speed(35)
                        print(alias, "going for the wagon")

    # initialize event listeners
    for train in trains:
        train_setup_function(train, shared_state, handle_wagon_ready)

    # start driving
    for train in trains:
        if not shared_state.trains[train.alias].waiting:
            train.drive_at_speed(35)

    input("When done, press Enter to exit...\n")

    # cleanup
    for train in trains:
        train.stop_driving()
        train.set_snap_command_execution(True)
        train.set_headlight_color()
        train.disconnect()


if __name__ == "__main__":
    main()
