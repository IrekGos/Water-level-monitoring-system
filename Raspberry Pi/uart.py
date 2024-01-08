import serial
from time import sleep
from dotenv import dotenv_values

CONFIG = dotenv_values(".env")

NUMBER_OF_SAMPLES = 3

uart = serial.Serial("/dev/ttyS0", 4800)


def send_data(data: str) -> None:
    to_be_sent = data + "\r\n"
    sent_bytes = uart.write(to_be_sent.encode('utf-8'))
    assert len(data) + 2 == sent_bytes


def receive_data() -> str:
    received_data = uart.read()
    sleep(0.1)
    data_left = uart.inWaiting()
    received_data += uart.read(data_left)
    return received_data.decode('utf-8')


def get_measurement_result() -> int:
    received_string = receive_data()
    received_data = []
    for i in range(NUMBER_OF_SAMPLES):
        received_data.append(int(received_string[i*3:(i+1)*3]))
    average = sum(received_data) / len(received_data)
    return int(average)


def connect_with_atmega() -> bool:
    send_data(CONFIG["SECRET_KEY"])
    response = receive_data()
    return bool(response)
