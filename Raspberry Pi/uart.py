import serial
from time import sleep
from dotenv import dotenv_values

CONFIG = dotenv_values(".env")

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
    received_data = receive_data()
    return int(received_data)


def connect_with_atmega() -> bool:
    send_data(CONFIG["SECRET_KEY"])
    response = receive_data()
    return bool(response)
