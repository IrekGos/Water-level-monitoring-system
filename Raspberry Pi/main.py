import logging
import argparse
from time import sleep
import leds
import uart
from keypad import KeyPad
from database import CredentialsDB
from cloud import send_data

WARNING_THRESHOLD = 450
ALERT_THRESHOLD = 500
MEASUREMENT_INTERVAL = 60


def logger_init():
    logging.basicConfig(filename="system.log",
                        format='[%(asctime)s] [%(levelname)s] %(message)s', filemode='a')
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    return logger


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--logging', action=argparse.BooleanOptionalAction)
    args = parser.parse_args()

    logging_enable = False
    if args.logging:
        logging_enable = True
        logger = logger_init()
        logger.info("System started")
        logger.info("Logging enabled")

    leds.led_init()

    keypad = KeyPad()
    print("Enter username: ", end='', flush=True)
    username = keypad.get_input()
    print("Enter password: ", end='', flush=True)
    password = keypad.get_input()

    db = CredentialsDB()
    user_successfully_authenticated = db.authenticate(username, password)
    if logging_enable:
        if user_successfully_authenticated:
            logger.info("The user has been successfully authenticated.")
        else:
            logger.error(
                "Username or password incorrect. Authentication failed. Exit")
    assert (user_successfully_authenticated == True)

    connection_established = uart.connect_with_atmega()
    if logging_enable:
        if connection_established:
            logger.info("Secret key is correct. Starting the measurement")
        else:
            logger.error("Secret key is incorrect")
    assert (connection_established == True)

    while True:
        result = uart.get_measurement_result()
        sent_correctly = send_data(result)
        if logging_enable:
            logger.info("Measurement result: %d" % result)
            if sent_correctly:
                logger.info(
                    "The result sent correclty to the ThingSpeak IoT cloud")
            else:
                logger.warning(
                    "Sending the result to the ThingSpeak IoT cloud failed")
        leds.default_leds_setting()
        if result > ALERT_THRESHOLD:
            leds.led_on(leds.RED_LED)
            leds.led_off(leds.GREEN_LED)
        elif result > WARNING_THRESHOLD:
            leds.led_on(leds.YELLOW_LED)
            leds.led_off(leds.GREEN_LED)
        sleep(MEASUREMENT_INTERVAL)
