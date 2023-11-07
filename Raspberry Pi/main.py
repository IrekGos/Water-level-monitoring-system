from time import sleep
import uart

MEASUREMENT_INTERVAL = 60

if __name__=="__main__":

    uart.connect_with_atmega()
    
    while True:
        res = uart.get_measurement_result()
        sleep(MEASUREMENT_INTERVAL)