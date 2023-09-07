from paho.mqtt import client as mqtt
import ssl, certifi

class Subscriber(mqtt.Client):

    def __init__(self):
        super().__init__()
        self.broker = 'test.mosquitto.org'
        self.port = 8885
        self.topic = "/api/#"

        self.username = 'ro'
        self.password = 'readonly'

        self.on_connect = self.on_connect
        self.on_subscribe = self.on_subscribe
        self.on_message = self.on_message
        
        self.tls_set(certifi.where(), None, None, cert_reqs=ssl.CERT_NONE, tls_version=ssl.PROTOCOL_TLSv1_2, ciphers=None)
        self.username_pw_set(self.username, self.password)
        self.connect(self.broker, self.port)

    def on_connect(self, client, userdata, flags, rc):
        print("Result from connect: {}".format(mqtt.connack_string(rc)))
        client.subscribe(self.topic, qos=2)

    def on_subscribe(self, client, userdata, mid, granted_qos):
        print("I've subscribed with QoS: {}".format(granted_qos[0]))

    def on_message(self, client, userdata, msg):
        print("Message received. Topic: {}. Payload: {}".format(msg.topic, str(msg.payload.decode('UTF-8'))))
    


if __name__  == '__main__':
    try:
        Subscriber().loop_forever()
    except KeyboardInterrupt:
        print('\nStop...')
        Subscriber().disconnect()
        Subscriber().loop_stop()