import time

from client import MQTTClient

last_message_time = time.time()
message_interval = 60
counter = 0


def callback_handler(topic, received_message):
    print(topic, received_message)


mqtt = MQTTClient("client_id", "username", "password", baudrate=115200)
mqtt.set_callback(callback_handler)

result, answer = mqtt.connect()

while not result:
    print(f"Connection result: {answer}")
    result, answer = mqtt.connect()
    time.sleep(1)

result = mqtt.subscribe("notifications")
print(answer)

while True:
    try:
        mqtt.check_message()

        if (time.time() - last_message_time) > message_interval:
            message = b'Time #%d' % counter
            mqtt.publish("time", message)

            last_message_time = time.time()
            counter += 1

    except Exception:
        mqtt.reconnect()
