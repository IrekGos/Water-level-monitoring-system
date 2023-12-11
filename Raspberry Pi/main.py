from time import sleep
import leds
import uart
import logging
import argparse

WARNING_TRESHOLD = 300
ALERT_TRESHOLD = 400
MEASUREMENT_INTERVAL = 60

def logger_init():
    logging.basicConfig(filename="results.log", format='%(levelname)s:%(asctime)s %(message)s', filemode='a')
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    return logger

if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--logging', action=argparse.BooleanOptionalAction)
    args = parser.parse_args()

    logging_enable = False
    if args.logging:
        logging_enable = True
        logger = logger_init()
        logger.info("Logging enabled")

    leds.led_init()

    connection_established = uart.connect_with_atmega()
    if logging_enable:
        if connection_established:
            logging.info("Secret key is correct. Starting the measurement")
        else:
            logging.info("Secret key is incorrect")
    assert(connection_established==True)
    
    while True:
        leds.default_leds_setting()
        res = uart.get_measurement_result()
        if logging_enable:
            logger.info("Measurement result: %d" % res)
        if res > ALERT_TRESHOLD:
            leds.led_on(leds.RED_LED)
            leds.led_off(leds.GREEN_LED)
        elif res > WARNING_TRESHOLD:
            leds.led_on(leds.YELLOW_LED)
            leds.led_off(leds.GREEN_LED)
        sleep(MEASUREMENT_INTERVAL)