import pymongo
import time
import paho.mqtt.client as mqtt
import json

MONGO_URI = "mongodb://localhost:27017/"
MONGO_DB = "mqtt_data"
MONGO_COLLECTION = "mqtt_messages"

class get_info():
    def __init__(self, cualTopic, token):
        self.mqtt_broker = "54.38.180.107"
        self.mqtt_user = "cogollo"
        self.mqtt_pass = "wasimodo98"
        self.mqtt_topic = cualTopic
        self.senToken = token
        self.respuesta = False
        self.fin = None
        self.mqtt_client = self.login_mqtt()

    def on_message(self, client, userdata, msg):
        message = msg.payload.decode("utf-8")
        if self.is_valid_json(message):
            recibido = json.loads(message)
            if 'token' in recibido and recibido['token'] == self.senToken:
                print(recibido)
                self.fin = recibido
                self.respuesta = True

    def is_valid_json(self, json_str):
        try:
            json.loads(json_str)
            return True
        except json.JSONDecodeError:
            return False

    def save_to_mongodb(self, topic, payload):
        client = pymongo.MongoClient(MONGO_URI)
        db = client[MONGO_DB]
        collection = db[MONGO_COLLECTION]

        document = {
            "topic": topic,
            "payload": payload
        }

        collection.insert_one(document)
        client.close()

    def login_mqtt(self):
        client = mqtt.Client()
        client.on_message = self.on_message
        client.username_pw_set(self.mqtt_user, password=self.mqtt_pass)
        client.connect(self.mqtt_broker, 1883, 60)
        client.subscribe(self.mqtt_topic)
        return client

    def take_info(self, timeout=55):
        try:
            self.mqtt_client.loop_start()
            self.mqtt_client.publish(self.mqtt_topic, "send " + self.senToken)

            start_time = time.time()
            while not self.respuesta and (time.time() - start_time) < timeout:
                time.sleep(1)

            if not self.respuesta:
                print("Timeout alcanzado, no se recibió respuesta.")
                return None

        except KeyboardInterrupt:
            print("\nSaliendo del programa.")
        finally:
            self.mqtt_client.loop_stop()
            self.mqtt_client.disconnect()

        return self.fin

# Ejemplo de uso
#if __name__ == "__main__":
    #sensor_info = get_info("sen_water_dist", "EfV6jrp5dedffMV")
    #data = sensor_info.take_info()
    #print(data)
