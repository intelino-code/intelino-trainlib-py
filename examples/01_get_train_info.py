"""
EXAMPLE 01: GET TRAIN INFO
---------------------------
TOPIC: Connecting to a train

SETUP: no track needed

NOTES: This simple example shows how to connect to your train and print available information.
"""
from intelino.trainlib import TrainScanner


def main():
    with TrainScanner() as train:
        print("Name:", train.name)
        print("ID:", train.id)
        print("Is connected:", train.is_connected)
        print("Current driving direction:", train.direction)
        print("Current speed [cm/s]:", train.speed_cmps)
        print("Next planned turn:", train.next_split_decision)
        print("Distance driven since connection [cm]:", train.distance_cm)


if __name__ == "__main__":
    main()
