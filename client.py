from _ast import Or
from enum import Flag, IntFlag
from typing import Optional


# from machine import UART, IDLE


class MQTTClient:
    PROTOCOL_NAME = "04MQTT"
    PROTOCOL_VERSION = "5"

    class MessageTypeAndFlags(IntFlag):
        CONNECT = 0b00010000
        CONNACK = 0b00100000
        DISCONNECT = 0b11100000

        SUBSCRIBE = 0b10000000
        SUBACK = 0b10010000
        UNSUBSCRIBE = 0b10100000
        UNSUBACK = 0b10110000

        PUBLISH = 0b00110000
        PUBACK = 0b01000000

        DUP = 0b1000
        QoS1 = 0b0010
        QoS2 = 0b0100
        QoS3 = 0b0110
        RETAIN = 0b0001
        NO_FLAGS = 0b0000

    class ConnectFlags(IntFlag):
        USERNAME = 0b10000000
        PASSWORD = 0b01000000
        CLEAR_SESSION = 0b00000010
        NO_FLAGS = 0b00000000

    def __init__(self, client_id: str, username, password, baudrate=None):
        # self.uart = UART(1, baudrate or 9600)  # init with given baudrate
        # self.uart.init(baudrate or 9600, 8, None, 1)  # init with given parameters
        # self.uart.irq(UART.RX_ANY, 5, self.uart_handler(), IDLE)

        self.callback = None

        self.client_id = client_id

        self.username = username
        self.password = password

    def change_address(self, new_client_id: str):
        self.client_id = new_client_id

    # ///////////////////////////////////////////////////////////////////////////////////////
    # def uart_read(self) -> Optional[bytes]:
    #     return self.uart.read()

    # def uart_write(self, data: bytes):
    #     self.uart.write(data)

    # def uart_handler(self):
    #     data = self.uart_read()
    #     print(data)

    # ///////////////////////////////////////////////////////////////////////////////////////
    def check_message(self):
        pass

    def set_callback(self, func):
        self.callback = func
        pass

    # ///////////////////////////////////////////////////////////////////////////////////////
    def connect(self):
        # Fixed Header
        fixed_header = self.MessageTypeAndFlags.CONNECT | self.MessageTypeAndFlags.NO_FLAGS

        # Variable Header
        # Protocol Name
        protocol_name = self.PROTOCOL_NAME
        # Protocol Version
        protocol_version = self.PROTOCOL_VERSION
        # Connect Flags
        connect_flags = self.ConnectFlags.USERNAME | self.ConnectFlags.PASSWORD | self.ConnectFlags.CLEAR_SESSION
        # Keep Alive
        keep_alive = 60
        # Properties
        # Length
        property_length = 5
        # Session Expiry Interval identifier
        identifier = 17
        # Session Expiry Interval
        expiry_interval = 60

        # Payload
        # Client id length
        client_id_length = len(self.client_id)
        client_id = self.client_id
        # Username length
        username_length = len(self.username)
        username = self.username
        # Password length
        password_length = len(self.password)
        password = self.password

        variable_header = ((protocol_name + protocol_version).encode() +
                           connect_flags.to_bytes(1, 'big') +
                           keep_alive.to_bytes(2, 'big') +
                           property_length.to_bytes(1, 'big') +
                           identifier.to_bytes(1, 'big') +
                           expiry_interval.to_bytes(4, 'big'))

        payload = (client_id_length.to_bytes(1, 'big') +
                   client_id.encode() +
                   username_length.to_bytes(1, 'big') +
                   username.encode() +
                   password_length.to_bytes(1, 'big') +
                   password.encode())

        # Fixed Header
        length = len(variable_header + payload)

        data = (fixed_header.to_bytes(1, 'big') + length.to_bytes(1, 'big') +
                variable_header + payload)
        # self.uart_write(data)

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
