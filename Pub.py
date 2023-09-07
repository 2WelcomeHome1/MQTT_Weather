from weather import get_weather as w
from paho.mqtt import client as mqtt
import ssl, certifi, time

class Publisher(mqtt.Client):
    def __init__(self):
        super().__init__()
        
        self.broker, self.port = 'test.mosquitto.org', 8885
        self.temptopic, self.status_topic = "/api/temperature/{}", '/api/status'

        self.username = 'rw' # 'wo'
        self.password = 'readwrite' # 'writeonly'
        self.weather_info, self.status = w().get_weather(merge = False) # merge = True
        self.stations = ['S50', 'S107', 'S60']

        self.on_connect = self.on_connect
        self.tls_set(certifi.where(), None, None, cert_reqs=ssl.CERT_NONE, tls_version=ssl.PROTOCOL_TLSv1_2, ciphers=None)
        self.username_pw_set(self.username, self.password)
        self.connect(self.broker, self.port)       

    def _tuple2str(self, tup):
        return ' '.join(str(x) for x in tup)
        
    def on_connect(self, client, userdata, flags, answ):
        print("Result from connect: {}".format(mqtt.connack_string(answ)))

    def _publish(self, client, topic, value):
        client.publish(topic, self._tuple2str(value)) if type(value) is tuple else client.publish(topic, value)
        time.sleep(1)
        
    def run(self):
        self._publish(self, self.status_topic, self.status)
        for station in self.stations: self._publish(self, self.temptopic.format(station), self.weather_info[station])
        time.sleep(5)



if __name__ == '__main__':
    try:
        print("Connecting to broker...")
        Publisher().loop_start()
        while True: Publisher().run()
    except KeyboardInterrupt:
        print('\nStop...')
        Publisher().disconnect()
        Publisher().loop_stop()