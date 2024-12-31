import pymongo
import time
import paho.mqtt.client as mqtt
import random
import json

MONGO_URI = "mongodb://localhost:27017/"
MONGO_DB = "mqtt_data"
MONGO_COLLECTION = "mqtt_messages"
#primer registro primiko pa darle info al sen y tal!!!
fin_info = None
class get_info_new():
    def __init__(self, cualTopic,new_topic,name,token,esp_cat):
        self.mqtt_broker = "54.38.180.107"
        self.mqtt_user = "cogollo"
        self.mqtt_pass = "wasimodo98"
        self.mqtt_topic = cualTopic
        self.new_topic = new_topic
        self.name = name
        self.token = token
        self.esp_cat = esp_cat
        self.respuesta = False
        self.fin = 0
        self.fin_new_data = None
        self.mqtt_client = self.login_mqtt()


    def on_connect(self, client, userdata, flags, rc):
        print("Conectado al broker MQTT con código de resultado "+str(rc))
        client.subscribe(self.mqtt_topic)
        print("Subscrito a:", self.mqtt_topic)

    def on_message(self, client,userdata, msg):
        #self.mqtt_client.loop_start()
        print(f"Mensaje recibido en el tema {msg.topic}: {msg.payload.decode('utf-8')}")
        if msg.payload.decode('utf-8') == "infoplss":
            send_data = {"topic":self.new_topic,"token":self.token,"name":self.name,"space":self.esp_cat}
            client.publish(msg.topic, str(send_data))
            #client.publish(msg.topic,"send")
            time.sleep(2)
            fin_info = send_data
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


    def take_info(self):
        try:
            self.client.loop_start()  # Iniciar bucle MQTT en un hilo separado

            while not self.respuesta:
                time.sleep(1)  # Esperar un segundo antes de verificar la respuesta

        except KeyboardInterrupt:
            print("\nSaliendo del programa.")
        finally:
            print("terminaossss mqtt")
            self.client.loop_stop()  # Detener el bucle MQTT
            self.client.disconnect()

        return self.fin

    def login_mqtt(self):
        #client_id = f'python-mqtt-{random.randint(0, 1000)}'
        self.client = mqtt.Client()
        self.client.on_message = self.on_message

        # Conectar con credenciales
        self.client.username_pw_set(self.mqtt_user, password=self.mqtt_pass)

        self.client.connect(self.mqtt_broker, 1883, 60)

        (result, mid) = self.client.subscribe(self.mqtt_topic)

        if result == mqtt.MQTT_ERR_SUCCESS:
            print(f"Suscrito al tema {self.mqtt_topic}")
        else:
            print(f"No se pudo suscribir al tema {self.mqtt_topic}. Creándolo...")
            # Si no se puede suscribir, publicamos un mensaje en el tema para crearlo
            self.client.publish(self.mqtt_topic, "Nuevo tema creado")

        #client.subscribe(self.mqtt_topic)
        #client.loop_start()
        self.take_info()
        return self.client


# Ejemplo de uso
#mqtt_topic = "senInfo"  # Cambia esto según tu necesidad
#info_instance = get_info(mqtt_topic,"sen_water_temp","testaco","testaco","sala22")
#respuesta_obtenida = info_instance.take_info()
#print(f'Respuesta obtenida: {respuesta_obtenida}')
