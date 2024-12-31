import hashlib
import json
import random
import string
import time
import requests

def create_hora(hora):
    split_hora = hora.split(":")
    num_hora = int(split_hora[0]) * 60 + int(split_hora[1])
    return num_hora


def sumar_dias(nombres_dias):
    dias = {
        "lunes": 0b10000001,
        "martes": 0b10000010,
        "miercoles": 0b10000100,
        "jueves": 0b10001000,
        "viernes": 0b10010000,
        "sabado": 0b10100000,
        "domingo": 0b11000000,
        "todos": 0b11111111
    }
    suma = 0
    for dia in nombres_dias:
        suma |= dias[dia]
    return suma, format(suma, '08b')

def rand_seq(allowed_chars, length):
    return ''.join(random.choice(allowed_chars) for _ in range(length))

def generate_signature(message_id, key, timestamp):
    combined = f"{message_id}{key}{timestamp}".encode('utf-8')
    return hashlib.md5(combined).hexdigest()


def generar_string_alfanumerico():
    caracteres = string.ascii_lowercase + string.digits  # Incluye letras minúsculas y números
    resultado = ''.join(random.choices(caracteres, k=16))  # Selecciona 16 caracteres al azar
    return resultado

def edit_packet_rutina(ip,device_uuid,channel,accion,key,week,times,enable,info_edit):
    message_id = rand_seq(string.hexdigits, 32).lower()
    #print(message_id)
    timestamp = int(time.time())
    signature = generate_signature(message_id, key, str(timestamp))
    packet = {
    "header": {
        "from": f"http://{ip}/config",
        "messageId": message_id,
        "method": "SET",
        "namespace": "Appliance.Control.TimerX",
        "payloadVersion": 1,
        "sign": signature,
        "timestamp": timestamp,
        "triggerSrc": "AndroidLocal",
        "uuid": device_uuid
    },
    "payload": {
        "timerx": {
            "week": week,
            "channel": channel,
            "type": 1,
            "sunOffset": 0,
            "duration": 0,
            "extend": {
                "toggle": {
                    "lmTime": 0,
                    "onoff": accion
                }
            },
            "createTime": timestamp,
            "enable": enable,
            "alias": info_edit['alias'],
            "id": info_edit['id_gen'],
            "time": times
        }
    }
}
    return json.dumps(packet, indent=4)

def create_packet_rutina(ip_address, name, device_uuid, channel, accion, key, week, times):
    message_id = rand_seq(string.hexdigits, 32).lower()
    #print(message_id)
    id_gen = generar_string_alfanumerico()
    timestamp = int(time.time())
    signature = generate_signature(message_id, key, str(timestamp))

    packet = {
    "header": {
        "from": f"http://{ip_address}/config",
        "messageId": message_id,
        "method": "SET",
        "namespace": "Appliance.Control.Multiple",
        "payloadVersion": 1,
        "sign": signature,
        "timestamp": timestamp,
        "triggerSrc": "AndroidLocal",
        "uuid": device_uuid
    },
    "payload": {
        "multiple": [
            {
                "payload": {
                    "timerx": {
                        "week": week,
                        "channel": channel,
                        "type": 1,
                        "sunOffset": 0,
                        "duration": 0,
                        "extend": {
                            "toggle": {
                                "channel": channel,
                                "onoff": accion
                            }
                        },
                        "createTime": timestamp,
                        "enable": 1,
                        "alias": name,
                        "id": id_gen,
                        "time": times
                    }
                },
                "header": {
                    "method": "SET",
                    "namespace": "Appliance.Control.TimerX"
                }
            }
        ]
    }
}
    return {'packet':json.dumps(packet, indent=4),'id_gen':id_gen,'alias':name}


def enviar_packet(packet, lanip):
    url = f"http://{lanip}/config"
    data_json = packet  # Convertir el paquete a una cadena JSON
    headers = {
        'Content-Type': 'application/json',
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate, br',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 7_9_4) AppleWebKit/601.22 (KHTML, like Gecko) Chrome/54.0.2981.111 Safari/603',
        'Connection': 'keep-alive',  # Usamos close para evitar problemas de keep-alive
        'Content-Length': str(len(data_json.encode('utf-8')))  # Calcular la longitud del contenido
    }

    print("URL:", url)
    print("Headers:", headers)
    print("Body:", data_json)

    try:
        response = requests.post(url, data=data_json, headers=headers, timeout=10)
        print(f"Respuesta del servidor: {response.status_code}, {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"Error al enviar la solicitud: {e}")

def manejo(info):
    data = info['info']
    hora_on = data['horario_on']
    hora_off = data['horario_off']
    aparatos = data['aparatos']
    channels = []
    if type(data['dias']) == list:
        dias = data['dias']
    else:
        dias = []
        for cada_dia in data['dias']:
            if data['dias'][cada_dia]:
                dias.append(cada_dia)
    print(aparatos)
    print('aparatos')
    for cada_channel in aparatos:
        print(cada_channel)
        channels.append(cada_channel['index'])
    lanip = data['lanip']
    d_uuid = data['uuid']
    nombre = data['nombre']
    userKey = data['userKey']
    hora_on_buena = create_hora(hora_on)
    hora_off_buena = create_hora(hora_off)
    horas_buenas = [hora_off_buena,hora_on_buena]
    semana_buena = sumar_dias(dias)[0]
    save_data = []
    #bucle channels y dentro bucle on y otro off de horas
    for num_ch, cada_canal in enumerate(channels):
        for num,cada_hora in enumerate(horas_buenas):
            if num == 0:
                nombre_edit = nombre+"_"+aparatos[num_ch]['name'].replace(" ","")+'_off'
            else:
                nombre_edit = nombre+"_"+aparatos[num_ch]['name'].replace(" ","")+'_on'
            packet = create_packet_rutina(lanip,nombre_edit,d_uuid,cada_canal,num,userKey,semana_buena,cada_hora)
            print(packet['id_gen'])
            print(packet['alias'])
            enviar_packet(packet['packet'], lanip)
            save_data.append({'alias':packet['alias'],'id_gen':packet['id_gen'],'channelInfo':cada_channel})
            time.sleep(10)
    return save_data

    #channel 0 es todo y onoff 0 es apagado

def editar(info):
    data = info['info']
    hora_on = data['horario_on']
    hora_off = data['horario_off']
    aparatos = data['aparatos']
    ids_rutinas = data['rutina_response']
    lanip = data['lanip']
    d_uuid = data['uuid']
    nombre = data['nombre']
    userKey = data['userKey']
    inf_rutinas = []
    dias = []
    channels = []
    if type(data['dias']) == list:
        dias = data['dias']
    else:
        dias = []
        for cada_dia in data['dias']:
            if data['dias'][cada_dia]:
                dias.append(cada_dia)
    for cada_channel in aparatos:
        channels.append(cada_channel['index'])
    for cada_id in range(0,len(ids_rutinas), 2):
        inf_rutinas.append([{'alias':ids_rutinas[cada_id]['alias'], 'id_gen': ids_rutinas[cada_id]['id_gen']},{'alias':ids_rutinas[cada_id+1]['alias'], 'id_gen': ids_rutinas[cada_id+1]['id_gen']}])

    hora_on_buena = create_hora(hora_on)
    hora_off_buena = create_hora(hora_off)
    horas_buenas = [hora_off_buena,hora_on_buena]
    semana_buena = sumar_dias(dias)[0]
    save_data = []
    for num_ch, cada_canal in enumerate(channels):
        print(cada_canal)
        for num,cada_hora in enumerate(horas_buenas):
            print(inf_rutinas[num_ch][num])
            packet = edit_packet_rutina(lanip,d_uuid,cada_canal,num,userKey,semana_buena,cada_hora,1,inf_rutinas[num_ch][num])
            enviar_packet(packet, lanip)
            save_data.append({'alias': inf_rutinas[num_ch][num]['alias'], 'id_gen': inf_rutinas[num_ch][num]['id_gen'],
                              'channelInfo': cada_channel})
            time.sleep(10)
        return save_data