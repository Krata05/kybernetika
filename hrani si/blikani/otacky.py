from machine import ADC, Pin
from rp2 import bootsel_button
from time import sleep_ms, ticks_diff, ticks_ms


# "AO": GP26 (physical pin 31); "DO": GP11 (physical pin 15).
SENSOR_OUTPUT = "AO"
CALIBRATION_MS = 6000
MIN_ADC_SPAN = 500

ring_power = Pin(9, Pin.OUT, value=0)
analog = SENSOR_OUTPUT == "AO"
sensor = ADC(Pin(26)) if analog else Pin(11, Pin.IN)
read_sensor = sensor.read_u16 if analog else sensor.value


def calibrate():
    print("Kalibrace: nech kolecko bezet a snimac mirit na jednu LED.")
    started = ticks_ms()
    low = high = read_sensor()
    while ticks_diff(ticks_ms(), started) < CALIBRATION_MS:
        if bootsel_button():
            print("Kalibrace zrusena.")
            return None
        value = read_sensor()
        low = min(low, value)
        high = max(high, value)
        sleep_ms(4)

    span = high - low
    print(f"Rozsah AO: {low} az {high}")
    if span < MIN_ADC_SPAN:
        print("Slaby signal. Pribliz snimac k LED nebo ho zastin.")
        return None
    return low + span * 2 // 5, low + span * 3 // 5


def measure(low, high):
    signal_min = signal_max = read_sensor()
    above = signal_min >= high
    last_edge = None
    last_signal = ticks_ms()
    while not bootsel_button():
        value = read_sensor()
        signal_min = min(signal_min, value)
        signal_max = max(signal_max, value)
        now = ticks_ms()
        if not above and value >= high:
            above = True
            if last_edge is not None:
                period_ms = ticks_diff(now, last_edge)
                print(f"{60000 / period_ms:.1f} ot/min | obeh {period_ms} ms")
            last_edge = last_signal = now
        elif above and value <= low:
            above = False

        if ticks_diff(now, last_signal) >= 6000:
            print(f"Bez zablesku. {SENSOR_OUTPUT}: {signal_min} az {signal_max} "
                  f"| prahy: {low} a {high}")
            signal_min = signal_max = value
            last_edge = None
            last_signal = now
        sleep_ms(4)


try:
    sensor_pin = "GP26, fyzicky pin 31" if analog else "GP11, fyzicky pin 15"
    print(f"Vstup: {SENSOR_OUTPUT} na {sensor_pin}")
    while True:
        print("Stiskni BOOTSEL pro spusteni mereni.")
        last_readout = ticks_ms()
        while not bootsel_button():
            now = ticks_ms()
            if ticks_diff(now, last_readout) >= 1000:
                print(f"Snimac v klidu: {SENSOR_OUTPUT} = {read_sensor()}")
                last_readout = now
            sleep_ms(15)
        while bootsel_button():
            sleep_ms(15)
        sleep_ms(30)

        ring_power.on()
        try:
            thresholds = calibrate() if analog else (0, 1)
            if thresholds is not None:
                print("Merim. Stiskni BOOTSEL pro zastaveni.")
                measure(*thresholds)
        finally:
            ring_power.off()

        while bootsel_button():
            sleep_ms(15)
        sleep_ms(30)
finally:
    ring_power.off()
