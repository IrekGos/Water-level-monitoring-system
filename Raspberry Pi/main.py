from time import sleep
import leds
import uart

WARNING_TRESHOLD = 300
ALERT_TRESHOLD = 400
MEASUREMENT_INTERVAL = 60

if __name__=="__main__":

    leds.led_init()

    uart.connect_with_atmega()
    
    while True:
        leds.default_leds_setting()
        res = uart.get_measurement_result()
        if res > ALERT_TRESHOLD:
            leds.led_on(leds.RED_LED)
            leds.led_off(leds.GREEN_LED)
        elif res > WARNING_TRESHOLD:
            leds.led_on(leds.YELLOW_LED)
            leds.led_off(leds.GREEN_LED)
        sleep(MEASUREMENT_INTERVAL)