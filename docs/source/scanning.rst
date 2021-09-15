Library Verification
=====================

After installing the ``intelino-trainlib`` package, you should verify that
everything installed successfully. First, make sure that Bluetooth is enabled
on your machine. Then power on your intelino smart train and run the
``intelino.scan`` utility:

.. code-block:: console

   $ python3 -m intelino.scan

If the Python environment works correcly, it should detect your train
and you will see the following information printed in the terminal:

.. code-block:: console

   Trains (1):
   xxxxxxxxxxxx : intelino J-1 (RSSI -XX)

   Others (x):
   ...

If your train doesn't show up in the list and there aren't any error meassages,
double-ckeck that Bluetooth is enabled and that your train isn't already
connected to your machine or another device.

.. note:: You do not need to pair/connect your train to your computer
   via Bluetooth Settings. That would make it invisible to the Python library.
   So, if you're having connection issues, open Bluetooth Settings on your
   computer and, if you see **'intelino J-1'** on the list of connected devices,
   remove it from that list.
