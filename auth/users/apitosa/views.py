from .serializers import *
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import get_authorization_header
from rest_framework.views import APIView
from rest_framework import status
import time
import secrets
from django.shortcuts import (get_object_or_404,render,HttpResponseRedirect)
from ..serializers import UserSerializer
from django.contrib import messages
from django.shortcuts import render, redirect
from rest_framework.exceptions import AuthenticationFailed
from ..authentication import create_access_token, create_refresh_token,decode_access_token,decode_refresh_token
from ..models import *


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_in(request):
    user = request.user
    info = user.show_info_set.all()
    serializer = show_info_serializer(info, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_in_hour(request):
    user = request.user
    info = user.register_new_hour_set.all()
    serializer = register_hour_serializer(info, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def get_data_op(request):
    print(request.data['elk'])
    user = request.user
    info = user.save_opcion_set.all()
    serializer = save_op(info, many=True)
    print(serializer.data)
    # meter conduicion solo enviar data de las opciones pedidas.
    return Response(serializer.data)

def delete(request, model, id):
    instance = get_object_or_404(model, id=id)
    instance.delete()
    instance.save()
    return Response(instance)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def save_data_op(request):
    #print(get_object_or_404(Save_opcion, id = 21))
    data = request.data['json']
    print("esto esd ata:")
    print(data)
    bypass_same = False
    serializer = ""
    if len(Save_opcion.objects.all()) > 0:
        for cada_save in Save_opcion.objects.all():
            #encontrado elk!
            print(cada_save)
            if data['elk'] == cada_save.json['elk']:
                saved = cada_save.json
                new = data
                for guardaos in saved:
                    #viejo
                    print(saved[guardaos])
                    #nuevo
                    print(new[guardaos])
                    if saved[guardaos] != new[guardaos]:
                        busca = get_object_or_404(Save_opcion, id=cada_save.id)
                        busca.delete()
                        serializer = save_op(data=request.data)
                        serializer.is_valid(raise_exception=True)
                        print(serializer)
                        serializer.save()
                    else:
                        bypass_same = True
            else:
                serializer = save_op(data=request.data)
                serializer.is_valid(raise_exception=True)
                print(serializer)
                serializer.save()
                print("guardao 2")
    else:
        serializer = save_op(data=request.data)
        serializer.is_valid(raise_exception=True)
        print(serializer)
        serializer.save()
        print("guardao 3")
    #cuando se guarda lo mismo no hay serializer
    if bypass_same:
        return Response(data)
    else:
        return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def hour_view_register(request):
    serializer = register_hour_serializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response()


class delete_hourss(APIView):
    def get(self,request,id):
        dele = Register_new_hour.objects.get(id=int(id))
        dele.delete()
        return Response()

@api_view(['GET'])
def get_info(request):
    auth = get_authorization_header(request).split()
    print('aquiiii:')
    print(auth)
    if auth and len(auth) == 2:
        print('entrar entra')
        print(request)
        token = auth[1].decode('utf-8')
        #aqui es donde dice desautentificado, linea de abajo
        id = decode_access_token(token)[0]
        print('lolaso')
        print(decode_access_token(token))
        user = User.objects.filter(pk=id).first()
        print('lol')
        return Response(UserSerializer(user).data)
    raise AuthenticationFailed('Desautentificado!lol')

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def API_add_space(request):
    if request.method == 'POST':
        # Obtén el token de autenticación del usuario actual
        user = request.user
        sensor_data = request.data
        sensor_data['user'] = user.id
        print(sensor_data)
        serializer = new_space(data=sensor_data)
        if serializer.is_valid():
            # Guarda el sensor en la base de datos, incluyendo nombre y fecha
            serializer.save()
            return Response({'message': 'Espacio registrado correctamente','nombre':sensor_data['nombre']}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def API_get_spaces(request):
    if request.method == 'GET':
        # Obtén el token de autenticación del usuario actual
        user = request.user
        info = NewSpace.objects.filter(user=user)
        print("yiiiiiiiiiiiiiiiiiija")
        print(info)
        serializer = new_space(info, many=True)
        return Response(serializer.data)


