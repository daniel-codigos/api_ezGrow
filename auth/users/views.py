from django.shortcuts import render


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import get_authorization_header
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenRefreshView,TokenObtainPairView
from .authentication import create_access_token, create_refresh_token,decode_access_token,decode_refresh_token
from .serializers import UserSerializer
from .models import User

import jwt,datetime
# Create your views here.




class MyTokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Añadir campos personalizados al token
        token['username'] = user.username
        token['superAdmin'] = user.is_superuser
        token['type'] = user.is_staff
        return token

    def validate(self, attrs):
        data = super().validate(attrs)

        refresh = self.get_token(self.user)

        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)

        # Añadir campos personalizados a la respuesta
        data['username'] = self.user.username
        data['superAdmin'] = self.user.is_superuser
        data['type'] = self.user.is_staff

        return data

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

class RegisterView(APIView):
    def post(self,request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

class LoginView(APIView):
    def post(self,request):
        #print(request.data)
        print('user:')
        print(request.user)
        email = request.data['username']
        password = request.data['password']
        user = User.objects.filter(username=email).first()
        if user is None:
            raise AuthenticationFailed('No se ha podido encontrar el usuaro!')
        if not user.check_password(password):
            raise AuthenticationFailed('Contraseña incorrecta ;(')

        access_token = create_access_token(user.id,email)
        refresh_token = create_refresh_token(user.id,email)
        resp = Response()

        #resp.set_cookie(key='refresh_token',value=refresh_token,httponly=True)
        resp.data = {
            'access':access_token,
            'refresh':refresh_token
        }
        return resp


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_verify(request):
    data = {'message': 'Esta es una respuesta desde el punto final protegido.'}
    return Response(data)

class UserView(APIView):
    def get(selfs,request):
        auth = get_authorization_header(request).split()
        if auth and len(auth) == 2:
            token = auth[1].decode('utf-8')
            id = decode_access_token(token)[0]

            user = User.objects.filter(pk=id).first()

            return Response(UserSerializer(user).data)
        raise AuthenticationFailed('Desautentificado!')

class LogoutView(APIView):
    def post(self,request):
        response = Response()
        response.delete_cookie('refresh_token')
        response.data = {
            'message':'success'
        }
        return response


class RefreshView(APIView):
    def post(self,request):
        #refresh_token = request.COOKIES.get("refresh_token")
        print(request.data)
        refresh_token = request.data["refresh"]
        data = decode_refresh_token(refresh_token)
        access_token = create_access_token(data[0],data[1])
        return Response({
            'access': access_token,
            #'refresh': refresh_token
        })



