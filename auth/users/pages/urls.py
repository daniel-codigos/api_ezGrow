from django.urls import path
from . import views


#views.API_sensor_temp_agua.as_view()
urlpatterns = [
    path('info_enchufes', views.API_info_enchufes),
    path('usar_enchufes', views.API_use_enchufes),
    path('editname_enchufes', views.API_editname_enchufes),
    path('tipo_aparato_enchufes', views.API_aparato_enchufes),
    path('info_aparatos', views.API_info_aparatos),
    path('save_meross', views.API_save_meross),
    path('del_aparato', views.API_del_aparato),
    #luz
    path('set_hora_luz', views.API_set_hora_luz),
    #riego
    path('set_riego', views.API_set_riego),
    path('info_riego', views.API_info_riego),
    path('lanzar_riego', views.API_lanzar_riego),
    path('infodb', views.API_infodb),
    path('config_capacidad', views.API_config_capacidad),
    path('set_bidones', views.API_set_bidones),
    path('info_bidones', views.API_info_bidones),
    path('rellenar_bidon', views.API_rellenar_bidon),
    #rutinas
    #que esta tambn mira pa editar o q hacer, sencillo
    path('crear_rutina', views.API_crear_rutina),
    path('ver_rutinas', views.API_ver_rutinas),
    path('del_rutinas', views.API_del_rutinas),
    #dashboard
    path('all_info_db', views.API_info_db_all),
    #nuevo cultivo
    path('nuevo_cultivo', views.API_new_culti),
]