# Human Interaction Recogniser

The recognisers are able to detect specific types of actions by humans in front of the cameras.
Different recognisers can have their own specialisations so that they in unison manage to cover
the full range of detections.

A recogniser must identify when an interaction starts and ends and with what confidence it is happening.

## Running multiple recognisers

If multiple recognisers are started they will all consume video and sensor inputs and produce event outputs. The system will take care of determining the final truth.

## Movement

- Walking towards
- Walking away
- Walking past


## States

- Sleeping Face
- Awake Face

## Gestures

- Waving
- Extending objects


## API

World Events are identified within a primary recording stream, such as a camera input.
The input is already know by the platform so it is simply referenced when recording the event.

Starting:

    func newEvent(recordingStream): WorldEvent
    WorldEvent.startTime = now()

or

    func recordEvent(): WorldEvent

Defining the event as it is recognised:

    WorldEvent.type = Gesturetype
    WorldEvent.confidence = 0.9
    
When the event is identified as completed the end time is set and it is now in the past and logged as such.

    WorldEvent.endTime = now()

    
