import pymongo
import time
import paho.mqtt.client as mqtt
import json

MONGO_URI = "mongodb://localhost:27017/"
MONGO_DB = "mqtt_data"
MONGO_COLLECTION = "mqtt_messages"

class get_info():
    def __init__(self, cualTopic,token):
        self.mqtt_broker = "54.38.180.107"
        self.mqtt_user = "cogollo"
        self.mqtt_pass = "wasimodo98"
        self.mqtt_topic = cualTopic
        self.senToken = token
        self.respuesta = False
        self.fin = 0
        self.mqtt_client = self.login_mqtt()

    def on_message(self, client, userdata, msg):
        message = msg.payload.decode("utf-8")
        # Verificar si la cadena es JSON válida
        if self.is_valid_json(message):
            recibido = json.loads(message)
            # Ahora puedes trabajar con el objeto JSON recibido
            if 'token' in recibido:
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

        # Conectar con credenciales
        client.username_pw_set(self.mqtt_user, password=self.mqtt_pass)

        client.connect(self.mqtt_broker, 1883, 60)
        client.subscribe(self.mqtt_topic)
        return client

    def take_info(self, timeout=50):
        try:
            self.mqtt_client.loop_start()  # Iniciar bucle MQTT en un hilo separado
            self.mqtt_client.publish(self.mqtt_topic, "send " + self.senToken)

            start_time = time.time()  # Marcar el tiempo inicial
            while not self.respuesta and (time.time() - start_time) < timeout:
                time.sleep(1)  # Esperar un segundo antes de verificar la respuesta nuevamente

            if not self.respuesta:
                print("Timeout alcanzado, no se recibió respuesta.")
                print(self.mqtt_topic)
                return None  # O manejar de alguna otra forma el timeout

        except KeyboardInterrupt:
            print("\nSaliendo del programa.")
        finally:
            self.mqtt_client.loop_stop()  # Detener el bucle MQTT
            self.mqtt_client.disconnect()

        return self.fin