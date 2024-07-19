from enum import Enum
from typing import Optional
from machine import UART, IDLE


class MQTTClient:

    class MessageType(Enum):
        CONNECT = 0b0001
        CONNACK = 0b0010
        DISCONNECT = 0b1110

        SUBSCRIBE = 0b1000
        SUBACK = 0b1001
        UNSUBSCRIBE = 0b1010
        UNSUBACK = 0b1011

        PUBLISH = 0b0011
        PUBACK = 0b0100

        def __or__(self, other):
            return self | other

    class Flags(Enum):
        DUP = 0b1000
        QoS1 = 0b0010
        QoS2 = 0b0100
        QoS3 = 0b0110
        RETAIN = 0b0001
        NO_FLAGS = 0b0000

        def __or__(self, other):
            return self | other

    class ConnectFlags(Enum):
        USERNAME = 0b10000000
        PASSWORD = 0b01000000
        NO_FLAGS = 0b00000000

        def __or__(self, other):
            return self | other

    def __init__(self, client_id: str, username, password, baudrate=None):
        self.uart = UART(1, baudrate or 9600)  # init with given baudrate
        self.uart.init(baudrate or 9600, 8, None, 1)  # init with given parameters
        self.uart.irq(UART.RX_ANY, 5, self.uart_handler(), IDLE)

        self.client_id = client_id

        self.mqtt_user = username
        self.mqtt_password = password

    def change_address(self, new_client_id: str):
        self.client_id = new_client_id

    # ///////////////////////////////////////////////////////////////////////////////////////
    def uart_read(self) -> Optional[bytes]:
        return self.uart.read()

    def uart_write(self, data: bytes):
        self.uart.write(data)

    def uart_handler(self):
        data = self.uart_read()
        print(data)

    # ///////////////////////////////////////////////////////////////////////////////////////
    def check_message(self):
        pass

    def set_callback(self, func):
        func("topic", "message")
        pass

    # ///////////////////////////////////////////////////////////////////////////////////////
    def connect(self):
        # Fixed Header
        fixed_header_byte1 = self.MessageType.CONNECT | self.Flags.NO_FLAGS
        fixed_header_byte2 = 16

        # Protocol Name
        variable_header_byte1 = 0
        variable_header_byte2 = 4
        variable_header_byte3 = b"M"
        variable_header_byte4 = b"Q"
        variable_header_byte5 = b"T"
        variable_header_byte6 = b"T"

        # Protocol Version
        variable_header_byte7 = 5

        # Connect Flags
        variable_header_byte8 = self.ConnectFlags.USERNAME | self.ConnectFlags.PASSWORD

        # Keep Alive
        variable_header_byte9 = 0
        variable_header_byte10 = 10

        # Properties
        # Length
        variable_header_byte11 = 5
        # Session Expiry Interval identifier
        variable_header_byte12 = 17
        # Session Expiry Interval
        variable_header_byte13 = 0
        variable_header_byte14 = 0
        variable_header_byte15 = 0
        variable_header_byte16 = 10

        data = bytes([fixed_header_byte1, fixed_header_byte2, variable_header_byte1, variable_header_byte2,
                      variable_header_byte3, variable_header_byte4, variable_header_byte5, variable_header_byte6,
                      variable_header_byte7, variable_header_byte8, variable_header_byte9, variable_header_byte10,
                      variable_header_byte11, variable_header_byte12, variable_header_byte13, variable_header_byte14,
                      variable_header_byte15, variable_header_byte16])

        self.uart_write(data)

        return True

    def disconnect(self):
        pass

    def reconnect(self):
        pass

    def subscribe(self, topic: str):
        pass

    def unsubscribe(self, topic: str):
        pass

    def publish(self, topic: str, message: bytes):
        # topic = "home/room/light", message = "on"/"off"
        pass
