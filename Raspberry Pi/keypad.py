from pad4pi import rpi_gpio

KEYPAD = [
    ["1", "2", "3"],
    ["4", "5", "6"],
    ["7", "8", "9"],
    ["*", "0", "#"]
]

ROW_PINS = [12, 16, 20, 21]  # BCM numbering
COL_PINS = [26, 19, 13]  # BCM numbering


class KeyPad:
    def __init__(self) -> None:
        factory = rpi_gpio.KeypadFactory()
        self.__keypad = factory.create_keypad(
            keypad=KEYPAD, row_pins=ROW_PINS, col_pins=COL_PINS)
        self.__keypad.registerKeyPressHandler(self.append_char)
        self.__buffer = ""
        self.__ready = False

    def append_char(self, key: str) -> None:
        if key == "#":
            self.__ready = True
        else:
            self.__buffer += key
            print(key, end='', flush=True)

    def get_input(self) -> str:
        while not self.__ready:
            pass
        self.__ready = False
        tmp = self.__buffer
        self.__buffer = ""
        print()
        return tmp

    def __del__(self) -> None:
        self.__keypad.cleanup()
