from .serializers import *
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from concurrent.futures import ThreadPoolExecutor, as_completed
from ..pages.models import *
from . import info_mqtt
from rest_framework.authentication import get_authorization_header
from rest_framework.views import APIView
from rest_framework import status
import calendar
import time
import json
from ..mqtt_sen_info import *
from django.shortcuts import (get_object_or_404,render,HttpResponseRedirect)
from django.contrib import messages
from django.shortcuts import render, redirect
from rest_framework.exceptions import AuthenticationFailed
from ..authentication import create_access_token, create_refresh_token,decode_access_token,decode_refresh_token
from ..models import *


class API_sensor_reg_data(APIView):
    #guardar info sensor temperatura agua en usuario (AGUA DE RIEGO, esto se guardará en cada riego )
    def post(self, request, format=None):
        # Verifica el token del ESP32
        esp32_token = request.META.get('HTTP_AUTHORIZATION', '').replace('Bearer ', '')
        try:
            current_GMT = time.gmtime()
            time_stamp = calendar.timegm(current_GMT)
            print(SaveNewSenInfo.objects.all())
            print(esp32_token)
            pre_info = SaveNewSenInfo.objects.all().values_list('info', flat=True)
            print(pre_info)
            for num,cada_info in enumerate(pre_info):
                if cada_info['token'] == esp32_token:
                    print(cada_info)
                    esp32_token_obj = SaveNewSenInfo.objects.all()[num]
                    obj_info = cada_info
                    print(num)
            #esp32_token_obj = SaveNewSenInfo.objects.get(info=esp32_token)
            print(esp32_token_obj)
            print(obj_info)
            user = esp32_token_obj.user.pk
            #test = SaveNewSenInfo.objects.filter(user=user)
            print("esto es test:")
            print(request.data['info'])
            info_final = {'user': user, 'name': request.data['info'], "space_name": obj_info['esp_cat'], 'timestamp': time_stamp, 'info': request.data}
            print(info_final)
            print(user)
            print(request.data)
            serializer = info_sensor(data=info_final)
            if serializer.is_valid():
                # Guarda el sensor en la base de datos, incluyendo nombre y fecha
                print("saaaa guardauuuuu, aunq aun no porq le has kitado q se guarde!!!")
                #serializer.save()
                return Response({'message': 'Sensor registrado correctamente', 'reg': info_final},
                                status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            return Response({'message': 'Token válido'})
        except InfoSensor.DoesNotExist:
            return Response({'message': 'Token no válido'}, status=status.HTTP_401_UNAUTHORIZED)
        # Tu lógica para procesar la solicitud aquí






@api_view(['post'])
@permission_classes([IsAuthenticated])
def NOW_API_sensor_temp_hume(request):
    if request.method == 'POST':
        #llamar con token
        mqtt_topic = "sen_temp_hm"  # Cambia esto según tu necesidad
        data = request.data['fin']
        user = request.user
        el_token = ''
        #SaveBidones.objects.filter(user=user)
        check_token = SaveNewSenInfo.objects.filter(user=user).values_list('info', flat=True)
        for cada_sen in check_token:
            if cada_sen['topic'] == mqtt_topic and cada_sen["esp_cat"] == data['space']:
                el_token = cada_sen['token']
                info_instance = get_info(mqtt_topic,el_token)
                respuesta_obtenida = info_instance.take_info()
                print(f'Respuesta obtenida: {respuesta_obtenida}')
                if respuesta_obtenida == None:
                    print("feo")
                    return Response({"Error": "TimeOut sensor"})
                else:
                    if len(data) > 1:
                        #tenemos registro de info valiosa
                        print(data['reg'])
                    return Response(respuesta_obtenida)
        return Response({"Error":"no se encontro el sensor en la db."})



@api_view(['post'])
@permission_classes([IsAuthenticated])
def NOW_API_level_water(request):
    mqtt_topic = "sen_lvl_w"  # Cambia esto según tu necesidad
    data = request.data['fin']
    user = request.user
    el_token = ''
    # SaveBidones.objects.filter(user=user)
    check_token = SaveNewSenInfo.objects.filter(user=user).values_list('info', flat=True)
    for cada_sen in check_token:
        if cada_sen['topic'] == mqtt_topic and cada_sen["esp_cat"] == data['space']:
            el_token = cada_sen['token']
            info_instance = get_info(mqtt_topic, el_token)
            respuesta_obtenida = info_instance.take_info()
            print(f'Respuesta obtenida: {respuesta_obtenida}')
            if respuesta_obtenida == None:
                print("feo")
                return Response({"Error": "TimeOut sensor"})
            else:
                if len(data) > 1:
                    # tenemos registro de info valiosa
                    print(data['reg'])
                return Response(respuesta_obtenida)
    return Response({"Error": "no se encontro el sensor en la db."})

@api_view(['post'])
@permission_classes([IsAuthenticated])
def API_info_tp_hm(request):
    user = request.user
    info = InfoSenTpHm.objects.filter(user=user)
    print("yiiiiiiiiiiiiiiiiiija")
    print(info)
    serializer = save_info_sen_tp_hm(info, many=True)
    return Response(serializer.data)

@api_view(['post'])
@permission_classes([IsAuthenticated])
def API_info_wlvl(request):
    user = request.user
    info = InfoSenWLevel.objects.filter(user=user)
    print(info)
    serializer = save_info_sen_wlvl(info, many=True)
    return Response(serializer.data)

@api_view(['post'])
@permission_classes([IsAuthenticated])
def API_take_info(request):
    if request.method == 'POST':
        user = request.user
        data = request.data['fin']
        print(data)
        info = SaveNewSenInfo.objects.filter(user=user)
        print(str(info))
        sen_space = []
        for cada in info:
            print(cada.info['esp_cat'])
            if cada.info['esp_cat'] == data['space']:
                sen_space.append(cada)
        serializer = save_new_info(sen_space, many=True)
        print(serializer.data)
        return Response(serializer.data)


@api_view(['post'])
@permission_classes([IsAuthenticated])
def API_save_new_info(request):
    #new info de new sensor
    print("vamos a guardar la info del nuevo sensor")
    print(request)
    user = request.user
    #data = json.loads(request.data)
    data = request.data
    print(request.data)
    topic_end = data["topic"]
    #mejor hacer el token aqui
    token = data['token']
    name = data['name']
    esp_cat = data["esp_cat"]
    info_mqtt.get_info_new("senInfo",topic_end,name,token,esp_cat)
    print("esti es lol jajaja")
    print(info_mqtt.fin_info)
    current_GMT = time.gmtime()
    time_stamp = calendar.timegm(current_GMT)
    json_data = {
        'topic': topic_end,
        'token': token,
        'name': name,
        'esp_cat': esp_cat
    }
    info_final = {'user': user.pk, 'info': json_data, 'timestamp': time_stamp}
    print(info_final)
    serializer = save_new_info(data=info_final)
    print(serializer)
    if serializer.is_valid():
        # Guarda el sensor en la base de datos, incluyendo nombre y fecha
        serializer.save()
        return Response({'message': 'Sensor registrado correctamente', 'reg': info_final},
                        status=status.HTTP_201_CREATED)
    else:
        print("error:")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response(info_final)


@api_view(['post'])
@permission_classes([IsAuthenticated])
def API_delete_sen(request):
    if request.method == 'POST':
        user = request.user
        data = request.data['fin']
        space = data['space']
        info = data['info']
        print(info)
        print(space)
        num_fin = 0
        info_sen = SaveNewSenInfo.objects.filter(user=user,info=info)
        print(info_sen)
        print(len(info_sen))
        if len(info_sen) == 1:
            if info_sen.values_list("info", flat=True)[0] == info:
                info_sen.delete()
        #info_sen[num_fin].delete()
            return Response({'success': 'deleted','info':info})
        else:
            return Response({'Error': 'Not found'})


@api_view(['post'])
@permission_classes([IsAuthenticated])
def NOW_API_sensores(request):
    if request.method == 'POST':
        data = request.data['fin']
        cual_sen = data['info']['token']
        mqtt_topic = data['info']['topic']
        user = request.user
        el_token = ''

        check_token = SaveNewSenInfo.objects.filter(user=user).values_list('info', flat=True)
        print("check_token:", check_token)
        for cada_sen in check_token:
            print("Processing sensor:", cada_sen)
            if cada_sen['name'] == data['info']['name'] and cada_sen["esp_cat"] == data['space'] and cada_sen['token'] == data['info']['token']:
                el_token = data['info']['token']
                print("Matching sensor found, token:", el_token)
                try:
                    print("Getting info for topic:", data['info']['topic'], "with token:", el_token)
                    info_instance = get_info(data['info']['topic'], el_token)
                    respuesta_obtenida = info_instance.take_info()
                    print("Response obtained:", respuesta_obtenida)
                    if respuesta_obtenida is None:
                        return Response({"Error": "TimeOut sensor"})
                    else:
                        respuesta_obtenida['name'] = data['info']['name']
                        return Response(respuesta_obtenida)
                except Exception as e:
                    print("Exception occurred:", str(e))
                    pass
        return Response({"Error": "no se encontro el sensor en la db."})

@api_view(['post'])
@permission_classes([IsAuthenticated])
def NOW_API_sensor_capacidad(request):
    if request.method == 'POST':
        data = request.data['fin']
        user = request.user
        el_token = ''
        check_token = SaveNewSenInfo.objects.filter(user=user).values_list('info', flat=True)
        inforiego = SaveRiego.objects.filter(user=user).values_list('info', flat=True)

        for cada_sen in check_token:
            if cada_sen['topic'] == inforiego[0]['senCap']['info']['topic'] and cada_sen["esp_cat"] == inforiego[0]['senCap']['info']['esp_cat'] and cada_sen['name'] == inforiego[0]['senCap']['info']['name']:
                el_token = cada_sen['token']
                try:
                    info_instance = get_info(inforiego[0]['senCap']['info']['topic'], el_token)
                    respuesta_obtenida = info_instance.take_info()
                    if respuesta_obtenida is None:
                        return Response({"Error": "TimeOut sensor"})
                    else:
                        return Response(respuesta_obtenida)
                except:
                    pass
        return Response({"Error": "no se encontro el sensor en la db."})

from concurrent.futures import ThreadPoolExecutor, as_completed

@api_view(['post'])
@permission_classes([IsAuthenticated])
def API_dashsen_all(request):
    if request.method == 'POST':
        user = request.user
        data = request.data['fin']
        print(data)
        info = SaveNewSenInfo.objects.filter(user=user)
        print(str(info))
        sen_space = []

        # Filtrar la información del espacio según el dato recibido
        for cada in info:
            print(cada.info['esp_cat'])
            if cada.info['esp_cat'] == data['space']:
                sen_space.append(cada)

        # Definir la función para procesar cada sensor
        def procesar_sensor(cada_sen):
            try:
                topic = cada_sen.info['topic']
                token = cada_sen.info['token']
                print(topic)
                print(token)

                info_instance = get_info(topic, token)
                respuesta_obtenida = info_instance.take_info()

                if respuesta_obtenida is None:
                    print("eerrorrrr primmm")
                else:
                    print("----------------------------------------------------")
                    print(respuesta_obtenida)
                    cada_sen.info['respuesta'] = respuesta_obtenida
                    print("----------------------------------------------------")
                return cada_sen
            except Exception as e:
                # Imprime el error para poder depurarlo
                print(f"Error en el bloque try: {e}")
                return None

        # Usar ThreadPoolExecutor para ejecutar múltiples procesos a la vez
        processed_sen_space = []
        with ThreadPoolExecutor(max_workers=5) as executor:
            future_to_sen = {executor.submit(procesar_sensor, cada_sen): cada_sen for cada_sen in sen_space}
            for future in as_completed(future_to_sen):
                result = future.result()
                if result:
                    processed_sen_space.append(result)

        # Serializar la información procesada
        serializer = save_new_info(processed_sen_space, many=True)
        print(serializer.data)
        return Response(serializer.data)
