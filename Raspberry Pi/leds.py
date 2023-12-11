import RPi.GPIO as GPIO

RED_LED = 17
YELLOW_LED = 27
GREEN_LED = 22


def led_on(led: int) -> None:
    GPIO.output(led, GPIO.HIGH)


def led_off(led: int) -> None:
    GPIO.output(led, GPIO.LOW)


def led_init() -> None:
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(RED_LED, GPIO.OUT)
    GPIO.setup(YELLOW_LED, GPIO.OUT)
    GPIO.setup(GREEN_LED, GPIO.OUT)


def default_leds_setting() -> None:
    led_on(GREEN_LED)
    led_off(YELLOW_LED)
    led_off(RED_LED)
