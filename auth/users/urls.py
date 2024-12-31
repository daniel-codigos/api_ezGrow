from django.contrib import admin
from django.urls import path, include
from .views import RegisterView, LoginView, UserView,LogoutView,RefreshView, MyTokenObtainPairView, get_verify
from rest_framework_simplejwt.views import TokenRefreshView
#from auth.apitosa import views


#minuto 31

urlpatterns = [
    path('register',RegisterView.as_view()),
    #path('login',LoginView.as_view()),
    path('login',MyTokenObtainPairView.as_view(), name='token_access'),
    path('user',UserView.as_view()),
    #aqui es la api de config y tal
    path('user2/',include('users.apitosa.urls')),
    #aqui api de sensores
    path('info_sensores/',include('users.info_sensores.urls')),
    path('pages/',include('users.pages.urls')),
    path('logout',LogoutView.as_view()),
    path('verify',get_verify),
    path('refresh',TokenRefreshView.as_view(), name='token_refresh')
    #path('refresh',RefreshView.as_view()),
]
