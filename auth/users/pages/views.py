import json
from .serializers import *
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import get_authorization_header
from rest_framework.views import APIView
import time
#from .rellenar import *
from .rutinas_meross import *
import calendar
from datetime import datetime
from ..lanzamos.test import *
import asyncio
from django.shortcuts import (get_object_or_404,render,HttpResponseRedirect)
from ..serializers import UserSerializer
from django.contrib import messages
from django.shortcuts import render, redirect
from rest_framework.exceptions import AuthenticationFailed
from ..authentication import create_access_token, create_refresh_token,decode_access_token,decode_refresh_token
from ..models import *
from .meross import *
from ..info_sensores.models import *
from ..info_sensores.serializers import *
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
#from .serializers import new_sensor  # Asegúrate de importar tu serializador


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def API_info_enchufes(request):
    if request.method == 'POST':
        #hacer checker
        print("holaa jaja")
        data = request.data['fin']
        print(data)
        user = request.user
        info = SaveMerossInfo.objects.filter(user=user)
        print(info)
        if len(info) > 0:
            serializer_meross = save_info_meross(info, many=True)
            cred = []
            print(serializer_meross.data)
            user_meross_info = None
            #check user
            for cada_data in serializer_meross.data:
                if cada_data['space'] == data['space']:
                    user_meross_info = cada_data
                    for key, value in cada_data.items():
                        print(f'Clave: {key}, Valor: {value}')
                        if key in ["email","passwd"]:
                            cred.append(value)
            #si tiene user:
            if len(cred):
                error = bool
                saca_lista_meross = meross_dev_list(cred[0],cred[1])
                if not "Error" in saca_lista_meross:
                    #status = main_status(cred[0],cred[1],saca_lista_meross[0]['type'])
                    print("no error putooooooooooooooooooooooo")
                    print(saca_lista_meross)
                    error = False
                    # regleta=mss425fc | enchfue indivisual = mss305
                    status = asyncio.run(check_status(cred[0],cred[1],["mss305","mss425fc"]))
                    print("cara colaaa")
                    print(status)
                else:
                    print("comete el error putooo jajajaj")
                    error = True
                    status = saca_lista_meross
                #guardamos esto en la db y ya modificamos, no?
                current_GMT = time.gmtime()
                time_stamp = calendar.timegm(current_GMT)
                fin = {"data":saca_lista_meross,"user_meross_info":user_meross_info,"status":status}
                db_status = SaveEnchuData.objects.filter(user=user)
                print("esto es db_status")
                print(db_status)
                print(len(db_status))
                print(data['space'])
                #print(db_status)
                flag_status = False
                for cada_regis in db_status:
                    if cada_regis.info['user_meross_info']['space'] == data['space']:
                        flag_status = True
                        print(cada_regis.info['user_meross_info']['space'])
                        for cada_meross in status:
                            print(cada_meross)
                            print(cada_regis.info['status'])
                            print(error)
                            if cada_meross in cada_regis.info['status']:
                                if not 'Error' in cada_regis.info['status'] or error == False:
                                    #podria servir guay esta linea de abajo pero cuando enciendo o apago no se actualiza en la db
                                    #status[cada_meross] = cada_regis.info['status'][cada_meross]
                                    for num,cada_regis_name in enumerate(cada_regis.info['status'][cada_meross]):
                                        print(cada_regis_name)
                                        print(status[cada_meross][num])
                                        if status[cada_meross][num]['name'] != cada_regis_name['name']:
                                            status[cada_meross][num]['name'] = cada_regis_name['name']
                                else:
                                    print("bar user carajo")
                                    return Response({'Error': 'bad user'})
                            else:
                                print("mla db, no coincide la db")
                    #print(cada_regis.info['status'])
                #print(status)
                if not flag_status:
                    print("flipis mi lokokokoko")
                    # Aquí creamos el nuevo registro de Meross si no existe
                    new_data = {
                        "user": user.id,
                        "info": {
                            "data": saca_lista_meross,  # Datos que recuperas de Meross
                            "user_meross_info": user_meross_info,  # Información de login de Meross
                            "status": status  # Estado de los dispositivos
                        },
                        "timestamp": time_stamp
                    }

                    # Creamos una nueva entrada en la base de datos para el usuario
                    serializer = save_enchufes_data(data=new_data)

                    if serializer.is_valid():
                        print("Guardando nueva entrada de Meross en la base de datos...")
                        serializer.save()
                        return Response(new_data)
                    else:
                        print("Error al guardar la nueva entrada de Meross en la base de datos")
                        return Response({"Error": "No se pudo guardar la nueva entrada en la base de datos"},
                                        status=400)
                info_final = {'user': user.id, 'info': fin, 'timestamp': time_stamp}
                check = SaveEnchuData.objects.filter(user=user)
                #print(check)
                #en caso de que no exista lo guarda!! debe de ser menor de 1
                if len(check) < 1:
                    serializer = save_enchufes_data(data=info_final)
                    if serializer.is_valid():
                        print("se guarda broderrr!")
                        serializer.save()
                        return Response(info_final)
                    else:
                        return Response({"Error":"error info"})
                else:
                    return Response(info_final)
            else:
                print("no hay info de login para este space!!")
                return Response({"Error": "error user space"})
        else:
            print("no lo tiene su paaaaapa")
            return Response({"Error": "error user"})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def API_editname_enchufes(request):
    if request.method == 'POST':
        user = request.user
        data = request.data
        print(user.id)
        info = SaveEnchuData.objects.filter(user_id=user.id)
        print(info)
        #if info.exists():
        if len(info) > 0:
            print("hola")
            for x in info:
                print("flipas")
                try:
                    # Intenta acceder a la información específica y actualizarla
                    print("vamos")
                    if data['regleta'] in x.info['status']:
                        print("entra")
                        x.info['status'][data['regleta']][data['numChannel']]['name'] = str(data['new_name'])
                        updated_info = x.info
                        print(json.dumps(updated_info))
                        print(type(updated_info))
                        SaveEnchuData.objects.filter(user_id=user.id).update(info=x.info)
                        return Response({'message': 'Información actualizada correctamente.'})
                    else:
                        # Si no se encuentra el índice específico, devuelve un error
                        return Response({'Error': 'La regleta o el canal especificado no existe.'}, status=400)
                except KeyError as e:
                    # Captura otros KeyErrors y devuelve un mensaje de error
                    return Response({'Error': f'KeyError: {e}'}, status=400)
            return Response({'message': 'Información actualizada correctamente.'})
        else:
            return Response({'Error': 'No se encontraron datos para este usuario.'}, status=404)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def API_set_hora_luz(request):
    if request.method == 'POST':
        #crear archivo luz.py
        user = request.user
        data = request.data
        current_GMT = time.gmtime()
        time_stamp = calendar.timegm(current_GMT)
        fin = {'user':user.id,'info':data,'timestamp':time_stamp,'space':data['space']}
        infoMeross = SaveMerossInfo.objects.filter(user_id=user.id)
        infoEnchu = SaveEnchuData.objects.filter(user_id=user.id)
        print(infoMeross)
        print(infoEnchu)
        info = SaveAparatoData.objects.filter(user_id=user.id)
        if len(info) > 0:
            for cada_aparato in info:
                if cada_aparato.info['space'] == data['space'] and cada_aparato.info['aparato'] == data['aparato'] and cada_aparato.info['regleta'] == data['regleta']:
                    #existe lo que kiere modificar
                    infoRutinas = TodasRutinas.objects.filter(user_id=user.id)
                    for cadaRutina in infoRutinas:
                        print(cadaRutina.info['aparatos'])
                    print(len(infoRutinas))
                    check_hora = SaveHora.objects.filter(user_id=user.id)
                    if len(check_hora) > 0:
                        # aqui vamos a modificar rutina de meross
                        #ya hya una hora creada, toca modificar
                        for cada_horario in check_hora:
                            if cada_horario.info['space'] == data['space'] and cada_horario.info['aparato'] == data['aparato']:
                                #modifica
                                SaveHora.objects.filter(user_id=user.id).update(info=data)
                            else:
                                #crea
                                serializer = save_hora(data=fin)
                                if serializer.is_valid():
                                    serializer.save()
                                    return Response(fin)
                        print("modificar hora ya creada con update jejajeja")
                    else:
                        #aqui vamos a crear nueva rutina de meross
                        #si no hay hora creada
                        serializer = save_hora(data=fin)
                        if serializer.is_valid():
                            serializer.save()
                            return Response(fin)
                # save meross rutina y test en db por si ya existe
        else:
            return Response({'Error':'No hay una lampara creada para modificar.'})
        return Response(fin)


    else:
        return Response({'Error': 'No se encontraron datos para este usuario.'})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def API_info_aparatos(request):
    if request.method == 'POST':
        data = request.data['fin']
        user = request.user
        info = SaveAparatoData.objects.filter(user_id=user.id)
        info_horas = SaveHora.objects.filter(user_id=user.id)
        info_status = SaveEnchuData.objects.filter(user_id=user.id)

        print("hola vamos con info aparatos")
        print(info)
        print("................................................")
        print(info_horas)
        print("................................................")
        print(info_status)
        print("................................................")
        print("lol1")
        # Se requiere que info_status tenga datos
        if len(info_status) > 0:
            # Variable para almacenar la información de status coincidente
            matched_status = None
            mirate = False
            print("lol2")
            # Bucle para verificar coincidencia en info_status con el espacio proporcionado
            for index,status in enumerate(info_status):
                print(status.info['user_meross_info']['space'])
                print(data['space'])
                if data['space'] == status.info['user_meross_info']['space']:
                    matched_status = index
                    mirate = True
                    break
            print("lol3")
            print(matched_status)
            # Si se encuentra coincidencia en info_status
            if mirate:
                # Serializamos solo el status coincidente
                print("looool--------------------------")
                print("lol1")
                for cada_hora in info_horas:
                    if cada_hora.info['space'] == data['space']:
                        serial_horas = save_hora(info_horas, many=True).data
                    else:
                        serial_horas = []
                print("lol4")
                for cada_aparato in info:
                    if cada_aparato.info['space'] == data['space']:
                        serial_aparatos = save_aparato_data(info, many=True).data
                    else:
                        serial_aparatos = []

                print("-------------------------------------------------------------------")
                print("info_aparatos:", serial_aparatos)
                print("info_horas:", serial_horas)
                print("info_status:", info_status[matched_status].info['status'])
                print("--------------------------------------------------------------------")

                return Response({
                    'info': serial_aparatos,
                    'info_horas': serial_horas,
                    'info_status': info_status[matched_status].info['status']
                    # Devolvemos solo la información del status coincidente
                })
            else:
                # Si no se encuentra coincidencia en info_status
                return Response(
                    {'Error': 'No se encontraron coincidencias en info_status para el espacio proporcionado.'},
                    status=400)
        else:
            # Si no hay datos en info_status
            return Response({'Error': 'No se encontraron datos en info_status para este usuario.'}, status=400)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def API_del_aparato(request):
    if request.method == 'POST':
        data = request.data
        user = request.user
        space = data ['space']
        numChannel = data['numChannel']
        aparato = data['aparato']
        regleta = data['regleta']
        print(data)
        instances = SaveAparatoData.objects.filter(user_id=user.id)
        if len(instances) > 1:
            for num,instance in enumerate(instances):
                # Accede a los datos dentro del campo JSON 'info'
                if instance.info['space'] == space and instance.info['regleta'] == regleta and instance.info['numChannel'] == numChannel and instance.info['aparato'] == aparato:
                    print(instance.timestamp)
                    SaveAparatoData.objects.filter(timestamp=instance.timestamp).delete()
                    print(instance)
                    #instance.delete()
                    #fin = {'user_id':user.id,'info':instance.info}
                    #print(SaveAparatoData.objects.filter(info=str(data)))
                    #fin.delete()
                    #instance.info.delete()
                    #print(SaveAparatoData.objects.filter(info=instance.info))
                    return Response({'success': 'deleted'})
        return Response({'Error':'not found'})
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def API_aparato_enchufes(request):
    if request.method == 'POST':
        user = request.user
        data = request.data
        space = data['space']
        print(user.id)
        info = SaveAparatoData.objects.filter(user_id=user.id)
        current_GMT = time.gmtime()
        time_stamp = calendar.timegm(current_GMT)
        final_data = {'user':user.id,'info':data,'timestamp':time_stamp,'space':space}
        print(info)
        if len(info) > 0:

            print("ya hay datos previossss")
            print("la movida mi lokok")
            print(info)
            check_save = bool
            for cada_info in info:
                print(cada_info)
                if cada_info.info['space'] == data['space'] and cada_info.info['regleta'] == data['regleta'] and cada_info.info['numChannel'] == data['numChannel']:
                    print("lokoooooooooooooooooooooo q si va siiii")
                    print(cada_info.info)
                    print(data)
                    print(SaveAparatoData.objects.filter(user_id=user.id,info=cada_info.info))
                    SaveAparatoData.objects.filter(user_id=user.id,info=cada_info.info).update(info=data)
                    check_save = True
                    return Response(final_data)
                else:
                    check_save = False
            if not check_save:
                print('nunca se ha guardado este')
                serializer = save_aparato_data(data=final_data)
                if serializer.is_valid():
                    print('se guarda!!')
                    if final_data['info']['aparato'] != '':
                        serializer.save()
                    return Response(final_data)

        else:
            print('nunca se ha guardado todo vacio')
            serializer = save_aparato_data(data=final_data)
            if serializer.is_valid():
                print('se guarda!!')
                serializer.save()
                return Response(final_data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def API_use_enchufes(request):
    if request.method == 'POST':
        user = request.user
        data = request.data['finalInfo']
        print("esto es lo q entra en accion para usar enchufe:")
        print(data)
        print(data['space'])
        info = SaveMerossInfo.objects.filter(user=user)
        print(info)
        if len(info) > 0:
            serializer = save_info_meross(info, many=True)
            cred = []
            for cada_space in serializer.data:
                if cada_space['space'] == data['space']:
                    for key, value in cada_space.items():
                        #print(f'Clave: {key}, Valor: {value}')
                        if key in ["email","passwd"]:
                            cred.append(value)

            print("aqui esta el errror:")
            print(cred[0])
            print(cred[1])
            print(cred)
            accion = asyncio.run(main_action(cred[0],cred[1],data))
            print("esto es lo q devuelve mi primoooooo la accion jeje")
            print(accion)
            if not 'Error' in accion:
                #try:
                db_data = SaveEnchuData.objects.filter(user_id=user.id)
                for cada_regis in db_data:
                    if data['regleta'] in cada_regis.info['status']:
                        print(cada_regis.info['status'][data['regleta']][data['channel']]['status'])
                        if accion['Succes'] == 'off':
                            cada_regis.info['status'][data['regleta']][data['channel']]['status'] = False
                        else:
                            cada_regis.info['status'][data['regleta']][data['channel']]['status'] = True
                return Response(accion)
            else:
                return Response({'Error':accion['Error']})
        else:
            return Response({"Error":"No se encontro ningun enchufe o regleta."})
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def API_save_meross(request):
    if request.method == 'POST':
        #hacer checker
        user = request.user
        data = request.data
        login = asyncio.run(main_login(data["email"],data["passwd"]))
        #test_login = meross_dev_login()
        if "Error" in login:
            return Response({'message': 'Error en el login.', 'details': login})
        else:
            check = SaveMerossInfo.objects.filter(user=user)
            current_GMT = time.gmtime()
            time_stamp = calendar.timegm(current_GMT)
            info_final = {'user': user.id, 'email': str(data["email"]), 'passwd':str(data["passwd"]), 'info':login['info'], 'timestamp': time_stamp, 'space':str(data["space"])}
            serializer = save_info_meross(data=info_final)
            if serializer.is_valid():
                serializer.save()

                return Response({'message': 'Login en Meross correcto. Guardado correctamente.'})
            else:
                return Response({'message': 'Error en la validación de datos.'})
        #return Response(data)



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def API_set_riego(request):
    if request.method == 'POST':
        user = request.user
        data = request.data
        current_GMT = time.gmtime()
        time_stamp = calendar.timegm(current_GMT)
        print(request.data)
        print(request)
        fin = {'user':user.id,'info':data,'timestamp':time_stamp,'space':data['space']}
        info = SaveAparatoData.objects.filter(user_id=user.id)
        print(fin)

        if len(info) > 0:
            for cada_aparato in info:
                if cada_aparato.info['space'] == data['space']:
                    #existe lo que kiere modificar
                    check_hora = SaveRiego.objects.filter(user_id=user.id)
                    if len(check_hora) > 0:
                        #ya hya una hora creada, toca modificar
                        print(check_hora)
                        for cada_horario in check_hora:
                            print("aqui cabronceteeeeee")
                            print(cada_horario.info)
                            print(data)
                            if cada_horario.info['space'] == data['space']:
                                SaveRiego.objects.filter(user_id=user.id).update(info=data)
                            else:
                                serializer = save_riego(data=fin)
                                if serializer.is_valid():
                                        # hacer pekeño check para int() de los horarios
                                    print('se guarda!!')
                                        # if final_data['info']['aparato'] != '':
                                    serializer.save()
                                    return Response(fin)
                        print("modificar hora ya creada con update jejajeja")
                    else:
                        serializer = save_riego(data=fin)
                        if serializer.is_valid():
                            #hacer pekeño check para int() de los horarios
                            print('se guarda!!')
                            # if final_data['info']['aparato'] != '':
                            serializer.save()
                            return Response(fin)
                    #riego_user_hora_diaHoy

                    print(cada_aparato)
                    print(data)
        else:
            return Response({'Error':'No hay una lampara creada para modificar.'})
        return Response(fin)
    else:
        return Response({'Error': 'No se encontraron datos para este usuario.'})


@api_view(['post'])
@permission_classes([IsAuthenticated])
def API_info_riego(request):
    if request.method == 'POST':
        user = request.user
        data = request.data['fin']
        info = SaveRiego.objects.filter(user=user)
        print("yiiiiiiiiiiiiiiiiiija")
        print(data)
        print(info)
        for cada_info in info:
            print(cada_info.info['space'])
            if cada_info.info['space'] == data['space']:

                serializer = save_riego(info, many=True)
                return Response(serializer.data)
        return Response({'Error':'No se ha encontrado riego config.'})

@api_view(['post'])
@permission_classes([IsAuthenticated])
def API_config_capacidad(request):
    if request.method == 'POST':
        user = request.user
        data = request.data['fin']


        return Response({"test":'test'})



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def API_set_bidones(request):
    if request.method == 'POST':
        user = request.user
        data = request.data['fin']
        current_GMT = time.gmtime()
        time_stamp = calendar.timegm(current_GMT)
        print(request.data)
        print(request)
        fin = {'user':user.id,'info':data,'timestamp':time_stamp}
        info = SaveAparatoData.objects.filter(user_id=user.id)
        print(fin)

        if len(info) > 0:
            for cada_aparato in info:
                if cada_aparato.info['space'] == data['space']:
                    #existe lo que kiere modificar
                    check_hora = SaveBidones.objects.filter(user_id=user.id)
                    if len(check_hora) > 0:
                        #ya hya una hora creada, toca modificar
                        for cada_horario in check_hora:
                            if cada_horario.info['space'] == data['space']:
                                SaveBidones.objects.filter(user_id=user.id).update(info=data)
                            else:
                                serializer = save_bidones(data=fin)
                                if serializer.is_valid():
                                    # hacer pekeño check para int() de los horarios
                                    print('se guarda!!')
                                    # if final_data['info']['aparato'] != '':
                                    serializer.save()
                                    return Response(fin)
                        print("modificar hora ya creada con update jejajeja")
                    else:
                        serializer = save_bidones(data=fin)
                        if serializer.is_valid():
                            #hacer pekeño check para int() de los horarios
                            print('se guarda!!')
                            # if final_data['info']['aparato'] != '':
                            serializer.save()
                            return Response(fin)
                    print(cada_aparato)
                    print(data)
        else:
            return Response({'Error':'No hay una lampara creada para modificar.'})
        return Response(fin)
    else:
        return Response({'Error': 'No se encontraron datos para este usuario.'})


@api_view(['post'])
@permission_classes([IsAuthenticated])
def API_info_bidones(request):
    if request.method == 'POST':
        user = request.user
        data = request.data['fin']
        info = SaveBidones.objects.filter(user=user)
        print("yiiiiiiiiiiiiiiiiiija2222")
        print(data)
        print(info)
        for cada_info in info:
            print(cada_info)
            print(data['space'])
            if cada_info.info['space'] == data['space']:
                print("aqui si entra kloooool")
                serializer = save_bidones(info, many=True)
                return Response(serializer.data)
        return Response({'Error':'No se ha encontrado bidones config.'})


@api_view(['post'])
@permission_classes([IsAuthenticated])
def API_infodb(request):
    if request.method == 'POST':
        print(request)
        user = request.user
        data = request.data['fin']
        btnName = data['btnName']
        space = data['space']
        print(btnName)
        fin_info = []
        if btnName == "DatosRiego":
            info = list(SaveLanzarRiego.objects.filter(user_id=user.id))
            serializer = save_lanzar_riego(info, many=True)
            donde = "info_riego"
        elif btnName == "DatosRelleno":
            info = list(SaveInfoRelleno.objects.filter(user_id=user.id))
            serializer = save_rellena(info, many=True)
            donde = "info_relleno"
            print("asd")
        print(info)

        for cada_serial in serializer.data:
            if cada_serial[donde]['space']:
                fin_info.append(cada_serial)
        #print(serializer)
        return Response({donde: fin_info}, status=status.HTTP_200_OK)
@api_view(['post'])
@permission_classes([IsAuthenticated])
def API_lanzar_riego(request):
    if request.method == 'POST':
        user = request.user
        data = request.data['fin']
        space = data['info_riego']['space']
        print(data['info_riego'])
        data['info_riego']['cantidadRiego'] = int(data['info_riego']['cantidadRiego']) * 1000
        now = datetime.now()
        temp_water = None
        capacidad = None
        time_stamp = datetime.timestamp(now)
        data['timestamp'] = time_stamp
        data['user'] = user.id
        #info = SaveBidones.objects.filter(user=user)
        print("yiiiiiiiiiiiiiiiiiija")
        print(data)
        print(now)
        print(time_stamp)
        print(datetime.fromtimestamp(time_stamp))
        serializer = save_lanzar_riego(data=data)
        if serializer.is_valid():
            serializer.save()
            print("-------------------------------------------------------")

            info = SaveAparatoData.objects.filter(user_id=user.id)
            inforiegodb = SaveRiego.objects.filter(user_id=user.id)
            save_meros = SaveMerossInfo.objects.filter(user_id=user.id)
            sensores = SaveNewSenInfo.objects.filter(user_id=user.id).values_list("info", flat=True)
            credenciales = [save_meros.values_list("email", flat=True)[0],
                            save_meros.values_list("passwd", flat=True)[0],
                            user.username]
            #print(inforiegodb[0]['info'])
            elsaveriego = []
            for cada_saveriego in inforiegodb.values_list("info", flat=True):
                print('lolaxo')
                print(cada_saveriego)
                if cada_saveriego['space'] == space:
                    elsaveriego.append(cada_saveriego)
            info_riego = data['info_riego']
            #info_riego['db_data'] = inforiegodb
            hora = data['info_riego']['horaRiegoStr']
            aparatos = info.values_list("info", flat=True)
            for cada_sensor in sensores:
                print(cada_sensor)
                print('sorpre1')
                if cada_sensor['esp_cat'] == space or info_riego['hardBypass']:
                    print(cada_sensor)
                    print('sorpre2')
                    if cada_sensor['topic'] == "sen_water_temp":
                        temp_water = cada_sensor
                    else:
                        temp_water = None
                    if cada_sensor['topic'] == "sen_water_dist":
                        capacidad = cada_sensor
                    else:
                        capacidad = None
            comentario = 'riego_'+user.username+"_"+hora.split(":")[0]+"_"+str(now.date().day)+str(now.date().month)
            datos = [credenciales,info_riego,aparatos,temp_water,capacidad,comentario,elsaveriego[0]]
            crear_archivos(comentario,hora,datos,script_code)
            # aqui llamamos a crear archivo y cron!!!
            # archivo,hora,datos
            # datos:
            # credenciales
            # info_riego
            # aparatos
            # temp_water
            # capacidad
            # comentario
            return Response({'Save': 'Guardado Correctamente!'})
        #print(info)
        else:
            return Response({'Error':"Info no puede ser guardada. Incorrecta."})
    else:
        return Response({'Error':'Error'})

@api_view(['post'])
@permission_classes([IsAuthenticated])
def API_rellenar_bidon(request):
    if request.method == 'POST':
        user = request.user
        data = request.data['fin']
        space = data['space']
        numLitros = data['cantidadRellenar']
        now = datetime.now()
        time_stamp = datetime.timestamp(now)
        fin = {'user':user.id, 'timestamp':time_stamp,'info_relleno':data}
        serializer = save_rellena(data=fin)
        if serializer.is_valid():
            serializer.save()
        else:
            print("no ha sido valido lo q kerias guarda lokooooo")
        print("yiiiiiiiiiiiiiiiiiija")
        print(data)
        print(now)
        print(time_stamp)
        print(datetime.fromtimestamp(time_stamp))
        print("-------------------------------------------------------")

        info = list(SaveAparatoData.objects.filter(user_id=user.id))
        save_meros = list(SaveMerossInfo.objects.filter(user_id=user.id))
        credenciales = [save_meros[0].email, save_meros[0].passwd, user.username]

        aparatos = [obj.info for obj in info]
        datos = [credenciales, aparatos]

        # Ejecuta lanzarRelleno en el loop asíncrono
        asyncio.run(lanzarRelleno(datos[0], datos[1], space, numLitros))

        return Response({'Save': 'Guardado Correctamente!'})
    else:
        return Response({'Error': "Info no puede ser guardada. Incorrecta."})

async def lanzarRelleno(credenciales, aparatos, spacename, numLitros):
    cuanto = int(numLitros) * 1000
    formula = (cuanto / 6300) * 60
    elegido = None
    for cada_aparato in aparatos:
        print(cada_aparato)
        if cada_aparato['aparato'] == "Bomba de rellenar":
            elegido = cada_aparato
            break

    print("-----------------------------------")
    sala_riego = spacename
    await asyncio.sleep(5)
    await main_action(credenciales[0], credenciales[1], {
        "regleta": elegido['regleta'],
        "channel": elegido['numChannel'],
        "aparato": elegido['aparato'],
        "space": sala_riego,
        "accion": "on"
    })
    await asyncio.sleep(formula)
    await main_action(credenciales[0], credenciales[1], {
        "regleta": elegido['regleta'],
        "channel": elegido['numChannel'],
        "aparato": elegido['aparato'],
        "space": sala_riego,
        "accion": "off"
    })
    await asyncio.sleep(10)
    print("Proceso completado.")


@api_view(['post'])
@permission_classes([IsAuthenticated])
def API_crear_rutina(request):
    if request.method == 'POST':
        user = request.user
        data = request.data['fin']
        now = datetime.now()
        time_stamp = datetime.timestamp(now)
        data['timestamp'] = time_stamp
        data['user'] = user.id
        space = data['info']['space']
        userKey = None
        infoMeross = SaveMerossInfo.objects.filter(user_id=user.id)
        if len(infoMeross) >= 1:
            print("vamos con todo bro")
            print(infoMeross)
            for cadaMeross in infoMeross:

                if cadaMeross.space == data['info']['space']:
                    print(json.loads(cadaMeross.info))
                    print(type(json.loads(cadaMeross.info)))
                    print(json.loads(cadaMeross.info)['key'])
                    userKey = json.loads(cadaMeross.info)['key']
                    print(userKey)
                    break

        if userKey != None:
            data['info']['userKey'] = userKey
            serializer = todas_rutinas(data=data)

            # {'lanip': '192.168.1.41', 'aparatos': [{'regleta': 'regleta1', 'numChannel': 2, 'aparato': 'Calentador agua', 'space': 'sala22'}, {'regleta': 'regleta1', 'numChannel': 5, 'aparato': 'Sensores', 'space': 'sala22'}], 'dias': {'lun
            # s': False, 'martes': False, 'miercoles': True, 'jueves': False, 'viernes': True, 'sabado': True, 'domingo': False}, 'horario': '15:20', 'uuid': '2303278087982854030348e1e9c25c67', 'nombre': 'Ggluz'}
            rutinas_save = TodasRutinas.objects.filter(user_id=user.id)
            print(rutinas_save)
            yaExiste = False
            for cada_rutina in rutinas_save:
                print("jooooooooooder")
                print(cada_rutina.info['nombre'])
                print(data['info']['nombre'])
                if cada_rutina.info['nombre'] == data['info']['nombre']:
                    yaExiste = True
                    data['info']['rutina_response'] = cada_rutina.info['rutina_response']
            if not yaExiste:
                if serializer.is_valid():
                    #serializer.save()
                    print("entramos bro")
                    meross_reg = manejo(data)
                    print(meross_reg)
                    data['info']['rutina_response'] = meross_reg
                    serializer2 = todas_rutinas(data=data)
                    if serializer2.is_valid():
                        serializer2.save()
                        return Response({'Save': 'Guardado Correctamente!'})
                #print(info)
                else:
                    return Response({'Error':"Info no puede ser guardada. Incorrecta."})
            else:
                if serializer.is_valid():
                    edita = editar(data)

                    checker = TodasRutinas.objects.filter(user_id=user.id)
                    print("---------------------------------------------")
                    for cada_buscakeda in checker.values_list('info', flat=True):
                        if cada_buscakeda['aparatos'] == data['info']['aparatos']:
                            print(cada_buscakeda)
                            chekk = checker.filter(info=cada_buscakeda)
                            chekk.update(info=data['info'])
                    return Response({'Save': 'Actualizado Correctamente!'})
    else:
        return Response({'Error':'Error'})

@api_view(['post'])
@permission_classes([IsAuthenticated])
def API_ver_rutinas(request):
    if request.method == 'POST':
        user = request.user
        data = request.data['fin']
        info = TodasRutinas.objects.filter(user=user)
        print("yiiiiiiiiiiiiiiiiiija")
        print(data)
        print(info)
        enviar = []
        for cada_info in info:
            print(cada_info.info['space'])
            print(data['space'])
            if cada_info.info['space'] == data['space']:
                enviar.append(cada_info)
        if len(enviar) > 0:
            serializer = save_bidones(enviar, many=True)
            return Response(serializer.data)
        else:
            return Response({'Error':'No se ha encontrado riego config.'})


@api_view(['post'])
@permission_classes([IsAuthenticated])
def API_del_rutinas(request):
    if request.method == 'POST':
        user = request.user
        data = request.data['fin']
        del_elem = data['del']
        space = data['space']
        info = TodasRutinas.objects.filter(user=user)
        print("yiiiiiiiiiiiiiiiiiija")
        print(del_elem['info']['nombre'])
        print(data)
        print(info)
        for index,cada_info in enumerate(info):
            if cada_info.info['space'] != space and del_elem['info']['nombre'] != cada_info.info['nombre']:
                info.remove(info[index])
            info.delete()
        return Response({'message': f'Producto "{del_elem["info"]["nombre"]}" eliminado correctamente'},
                        status=status.HTTP_200_OK)

@api_view(['post'])
@permission_classes([IsAuthenticated])
def API_info_db_all(request):
    if request.method == 'POST':
        if request.method == 'POST':
            print(request)
            user = request.user
            data = request.data['fin']
            space = data['space']
            fin_info_riego = []
            fin_info_rellena = []
            info = list(SaveLanzarRiego.objects.filter(user_id=user.id))
            serializer = save_lanzar_riego(info, many=True)
            donde = "info_riego"
            info2 = list(SaveInfoRelleno.objects.filter(user_id=user.id))
            serializer2 = save_rellena(info2, many=True)
            donde2 = "info_relleno"
            print(info)
            for cada_serial in serializer.data:
                if cada_serial[donde]['space'] == space:
                    fin_info_riego.append(cada_serial)
            for cada_serial2 in serializer2.data:
                print(cada_serial2)
                if cada_serial2[donde2]['space'] == space:
                    fin_info_rellena.append(cada_serial2)
            # print(serializer)
            print("esto es info riego")

            return Response({donde: fin_info_riego, donde2:fin_info_rellena}, status=status.HTTP_200_OK)






@api_view(['post'])
@permission_classes([IsAuthenticated])
def API_new_culti(request):
    if request.method == 'POST':
        user = request.user
        data = request.data
        nombre = data['nombreCultivo']
        guardamos = data['guardarDatosAntiguo']
        space = data['space']
        current_GMT = time.gmtime()
        time_stamp = calendar.timegm(current_GMT)
        # Crear listas de los elementos para backup
        infoLanzarRiego = SaveLanzarRiego.objects.filter(user_id=user.id)
        infoInfoRelleno = SaveInfoRelleno.objects.filter(user_id=user.id)
        infoNewSenInfo = SaveNewSenInfo.objects.filter(user_id=user.id)
        infoAparatoData = SaveAparatoData.objects.filter(user_id=user.id,info__space=space)
        infoBidones = SaveBidones.objects.filter(user_id=user.id)
        infoRiego = SaveRiego.objects.filter(user_id=user.id)

        # Serializar los datos
        serializer_lanzar_riego = save_lanzar_riego(infoLanzarRiego, many=True)
        serializer_info_relleno = save_rellena(infoInfoRelleno, many=True)
        serializer_new_sen_info = save_new_info(infoNewSenInfo, many=True)
        serializer_aparato_data = save_aparato_data(infoAparatoData, many=True)
        serializer_bidones = save_bidones(infoBidones, many=True)
        serializer_riego = save_riego(infoRiego, many=True)

        # Crear un JSON bonito con los datos de backup
        backup_data = {
            "user": user.id,
            "nombre_culti":nombre,
            "space":space,
            "finalizado":time_stamp,
            "bk": {
                "info_new_sen_info": serializer_new_sen_info.data,
                "info_aparato_data": serializer_aparato_data.data,
                "info_bidones": serializer_bidones.data,
                "info_data_riego": serializer_riego.data,
                "info_riegos": serializer_lanzar_riego.data,
                "info_relleno": serializer_info_relleno.data
            }
        }

        # Guardar el JSON en SaveOldCulti
        print(guardamos)
        if guardamos:
            SaveOldCulti.objects.create(user=user, info=backup_data)
            # Intenta guardar solo una parte más simple del JSON para ver si funciona
           # SaveOldCulti.objects.create(user=user, info={"simple_key": "simple_value"})

        # Eliminar los elementos de la sección "borrar"
        infoLanzarRiego.delete()
        infoInfoRelleno.delete()

        return Response({"message": "Backup guardado y datos eliminados correctamente."})
