# Awakeness

While awake Ziloo can be in an activity. This will keep it awake until the battery is very low,
and it will be forced to abort the activity.

If Ziloo isn't in an activity it will enter rest after 1 minute

## Resting state

During resting state,

- Cameras are only polled at 1fps
- Only one camera is on
- Microphone is turned off


## Waking up from resting state

Once resting Ziloo will wake up if,

- Human Body sensor senses changes
- Accelerometor senses being moved
- NFC sensor detects card
- *Stem* detects movement via sensors in Occi (gesture detector? proximity? color?)


## Entering resting state

When Ziloo is away it will enter resting state if,

- No activity(specific mode) is going on, and
- No human present for 5 minutes, or
- No gestures/interaction for 15 minutes


## Sleeping state

During sleeping state,

- GPU / NPU are switched off
- CPU is set to run at 100MHz
- Cameras are switched off
- Recogniser processes are given no input
- MPP Tasks are paused


## Entering Sleep

Ziloo will enter sleep if

- Low battery power
- Within a mandatory sleep period in account calendar
- Within a sleep until period in account settings
- If light is switched off for more than 5 minutes and there is no movement


## Waking up from sleep

Unless the battery is *not* low, once asleep Ziloo will wake up if

- Human Body sensor senses changes
- Accelerometor senses being moved
- NFC sensor detects card



## Low battery

Ziloo cannot start or do an activy during low battery.

