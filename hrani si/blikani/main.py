from machine import Pin
from neopixel import NeoPixel
from random import randint
from rp2 import bootsel_button
from time import sleep_ms, ticks_diff, ticks_ms


leds = (
    Pin(13, Pin.OUT, value=0),  # red
    Pin(14, Pin.OUT, value=0),  # yellow
    Pin(15, Pin.OUT, value=0),  # green
)
pixel = NeoPixel(Pin(8), 1)
ring_power = Pin(9, Pin.OUT, value=0)

# Each phase contains the three LED states and the matching RGB color.
TRAFFIC_PHASES = (
    ((0, 0, 1), (0, 32, 0)),
    ((0, 1, 0), (32, 24, 0)),
    ((1, 0, 0), (32, 0, 0)),
    ((1, 1, 0), (32, 8, 0)),
)
CHASE = (0, 1, 2, 1)
SHOW_INTERVALS_MS = (45, 25, 75)
DEBOUNCE_MS = 30
LONG_PRESS_MS = 700
TRAFFIC, SHOW, ROULETTE, COUNTDOWN, RHYTHM = range(5)
ROULETTE_LIGHTS = (
    ((1, 0, 0), (32, 0, 0)),
    ((0, 1, 0), (32, 24, 0)),
    ((0, 0, 1), (0, 32, 0)),
)
COUNTDOWN_IDLE = ((0, 0, 0), (0, 0, 32))
COUNTDOWN_PHASES = (
    (0, ROULETTE_LIGHTS[0]),
    (3000, ROULETTE_LIGHTS[1]),
    (5000, ROULETTE_LIGHTS[2]),
)
COUNTDOWN_END_MS = 8000
RHYTHM_IDLE = ((0, 0, 0), (0, 24, 24))
RHYTHM_PAUSE_MS = 1300
RHYTHM_FLASH_MS = 90


def display(states, color):
    for led, state in zip(leds, states):
        led.value(state)
    pixel[0] = color
    pixel.write()


def rainbow(frame):
    intensity = 32
    segment, fade = divmod(frame % (3 * intensity), intensity)
    return (
        (intensity - fade, fade, 0),
        (0, intensity - fade, fade),
        (fade, 0, intensity - fade),
    )[segment]


def spin_roulette():
    winner = randint(0, 2)
    delays = (60, 60, 60, 75, 90, 115, 150, 200, 280, 420)
    ring_power.on()
    for step, delay in enumerate(delays):
        position = (winner + step - len(delays) + 1) % len(ROULETTE_LIGHTS)
        display(*ROULETTE_LIGHTS[position])
        sleep_ms(delay)
    ring_power.off()

    if winner == 2:
        for _ in range(3):
            display((0, 0, 0), (0, 0, 0))
            sleep_ms(120)
            display(*ROULETTE_LIGHTS[winner])
            sleep_ms(120)


phase = 0
phase_started = ticks_ms()
mode = TRAFFIC
speed = 0
frame = 0
last_frame = ticks_ms()
countdown_started = None
countdown_phase = 0
tap_offsets = []
first_tap = 0
last_tap = 0
replay_started = None
replay_beat = 0
flash_started = None

raw_pressed = stable_pressed = bool(bootsel_button())
raw_changed = ticks_ms()
pressed_at = raw_changed

try:
    display(*TRAFFIC_PHASES[phase])
    while True:
        now = ticks_ms()

        if phase % 2 and ticks_diff(now, phase_started) >= 1000:
            phase = (phase + 1) % len(TRAFFIC_PHASES)
            if mode == TRAFFIC:
                display(*TRAFFIC_PHASES[phase])

        pressed = bool(bootsel_button())
        if pressed != raw_pressed:
            raw_pressed = pressed
            raw_changed = now

        if raw_pressed != stable_pressed and ticks_diff(now, raw_changed) >= DEBOUNCE_MS:
            stable_pressed = raw_pressed
            if stable_pressed:
                pressed_at = raw_changed
            elif ticks_diff(raw_changed, pressed_at) >= LONG_PRESS_MS:
                mode = (mode + 1) % 5
                countdown_started = None
                tap_offsets.clear()
                replay_started = None
                flash_started = None
                ring_power.value(mode == SHOW)
                if mode == SHOW:
                    frame = 0
                    last_frame = None
                elif mode == ROULETTE:
                    display((0, 0, 0), (22, 0, 32))
                elif mode == COUNTDOWN:
                    display(*COUNTDOWN_IDLE)
                elif mode == RHYTHM:
                    display(*RHYTHM_IDLE)
                else:
                    display(*TRAFFIC_PHASES[phase])
            elif mode == SHOW:
                speed = (speed + 1) % len(SHOW_INTERVALS_MS)
            elif mode == ROULETTE:
                spin_roulette()
            elif mode == COUNTDOWN:
                if countdown_started is None:
                    countdown_started = now
                    countdown_phase = 0
                    display(*COUNTDOWN_PHASES[0][1])
                else:
                    countdown_started = None
                    ring_power.off()
                    display(*COUNTDOWN_IDLE)
            elif mode == RHYTHM:
                if replay_started is None:
                    if not tap_offsets:
                        first_tap = pressed_at
                    tap_offsets.append(ticks_diff(pressed_at, first_tap))
                    last_tap = now
            elif phase % 2 == 0:
                phase += 1
                phase_started = now
                display(*TRAFFIC_PHASES[phase])

        if mode == SHOW and (last_frame is None or ticks_diff(now, last_frame) >= SHOW_INTERVALS_MS[speed]):
            active = CHASE[(frame // 4) % len(CHASE)]
            display((active == 0, active == 1, active == 2), rainbow(frame))
            frame = (frame + 1) % 96
            last_frame = now

        if countdown_started is not None:
            elapsed = ticks_diff(now, countdown_started)
            if elapsed >= COUNTDOWN_END_MS:
                countdown_started = None
                ring_power.off()
                display(*COUNTDOWN_IDLE)
            elif countdown_phase < 2:
                next_at, lights = COUNTDOWN_PHASES[countdown_phase + 1]
                if elapsed >= next_at:
                    countdown_phase += 1
                    display(*lights)
                    if countdown_phase == 2:
                        ring_power.on()

        if mode == RHYTHM and tap_offsets:
            if replay_started is None and (
                len(tap_offsets) >= 12
                or (not raw_pressed and ticks_diff(now, last_tap) >= RHYTHM_PAUSE_MS)
            ):
                replay_started = now
                replay_beat = 0
                ring_power.on()

            if replay_started is not None:
                elapsed = ticks_diff(now, replay_started)
                if replay_beat < len(tap_offsets) and elapsed >= tap_offsets[replay_beat]:
                    display(*ROULETTE_LIGHTS[replay_beat % len(ROULETTE_LIGHTS)])
                    flash_started = now
                    replay_beat += 1
                elif flash_started is not None and ticks_diff(now, flash_started) >= RHYTHM_FLASH_MS:
                    flash_started = None
                    if replay_beat == len(tap_offsets):
                        tap_offsets.clear()
                        replay_started = None
                        ring_power.off()
                        display(*RHYTHM_IDLE)
                    else:
                        display((0, 0, 0), (0, 0, 0))

        sleep_ms(5)
finally:
    ring_power.off()
    display((0, 0, 0), (0, 0, 0))
