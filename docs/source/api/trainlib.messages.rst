Messages (from the train)
=========================

The intelino train sends a lot of valuable information which is accessible
through typed data classes (read only). Some of this information comes as
events and some are delivered as responses to single requests or stream
requests.

Base classes
------------

Base classes are not intended for use, but it is good to know what have
all messages in common.

.. autoclass:: trainlib.messages.TrainMsgBase()
   :members:
   :inherited-members:
   :member-order: bysource

.. autoclass:: trainlib.messages.TrainMsgEventBase()
   :members:
   :inherited-members:
   :show-inheritance:
   :member-order: bysource

.. autoclass:: trainlib.messages.TrainMsgEventSensorColorChangedBase()
   :members:
   :inherited-members:
   :show-inheritance:
   :member-order: bysource

Response messages
-----------------

.. autoclass:: trainlib.messages.TrainMsgMacAddress()
   :members:
   :inherited-members:
   :show-inheritance:
   :member-order: bysource

.. autoclass:: trainlib.messages.TrainMsgTrainUuid()
   :members:
   :inherited-members:
   :show-inheritance:
   :member-order: bysource

.. autoclass:: trainlib.messages.TrainMsgVersionDetail()
   :members:
   :inherited-members:
   :show-inheritance:
   :member-order: bysource

.. autoclass:: trainlib.messages.TrainMsgStatsLifetimeOdometer()
   :members:
   :inherited-members:
   :show-inheritance:
   :member-order: bysource

.. autoclass:: trainlib.messages.TrainMsgMovement()
   :members:
   :inherited-members:
   :show-inheritance:
   :member-order: bysource

Event messages
--------------

.. autoclass:: trainlib.messages.TrainMsgEventMovementDirectionChanged()
   :members:
   :inherited-members:
   :show-inheritance:
   :member-order: bysource

.. autoclass:: trainlib.messages.TrainMsgEventLowBattery()
   :members:
   :inherited-members:
   :show-inheritance:
   :member-order: bysource

.. autoclass:: trainlib.messages.TrainMsgEventChargingStateChanged()
   :members:
   :inherited-members:
   :show-inheritance:
   :member-order: bysource

.. autoclass:: trainlib.messages.TrainMsgEventButtonPressDetected()
   :members:
   :inherited-members:
   :show-inheritance:
   :member-order: bysource

.. autoclass:: trainlib.messages.TrainMsgEventSnapCommandDetected()
   :members:
   :inherited-members:
   :show-inheritance:
   :member-order: bysource

.. autoclass:: trainlib.messages.TrainMsgEventSnapCommandExecuted()
   :members:
   :inherited-members:
   :show-inheritance:
   :member-order: bysource

.. autoclass:: trainlib.messages.TrainMsgEventFrontColorChanged()
   :members:
   :inherited-members:
   :show-inheritance:
   :member-order: bysource

.. autoclass:: trainlib.messages.TrainMsgEventBackColorChanged()
   :members:
   :inherited-members:
   :show-inheritance:
   :member-order: bysource

.. autoclass:: trainlib.messages.TrainMsgEventSplitDecision()
   :members:
   :inherited-members:
   :show-inheritance:
   :member-order: bysource


Error messages
--------------

.. autoclass:: trainlib.messages.TrainMsgUnknown()
   :members:
   :inherited-members:
   :show-inheritance:
   :member-order: bysource

.. autoclass:: trainlib.messages.TrainMsgEventUnknown()
   :members:
   :inherited-members:
   :show-inheritance:
   :member-order: bysource

.. autoclass:: trainlib.messages.TrainMsgMalformed()
   :members:
   :inherited-members:
   :show-inheritance:
   :member-order: bysource

Union classes
-------------

The library defines aliased union classes for messages. These should be used
instead of the base classes e.g. when a function expects various message types
as arguments.

.. autoclass:: trainlib.messages.TrainMsg
   :members:
   :inherited-members:
   :member-order: bysource

.. autoclass:: trainlib.messages.TrainMsgEvent
   :members:
   :inherited-members:
   :member-order: bysource

.. autoclass:: trainlib.messages.TrainMsgEventSensorColorChanged
   :members:
   :inherited-members:
   :member-order: bysource
