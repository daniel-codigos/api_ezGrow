from django.urls import path
from . import views


#views.API_sensor_temp_agua.as_view()
urlpatterns = [
    #path('temp_agua', views.API_sensor_temp_agua.as_view()),
    #registrar info
    path('temp_hume', views.API_sensor_reg_data.as_view()),
    path('now_temp_hume', views.NOW_API_sensor_temp_hume),
    path('now_info_capacidad', views.NOW_API_sensor_capacidad),
    path('now_info_sensor', views.NOW_API_sensores),
    path('save_new_info', views.API_save_new_info),
    path('take_info', views.API_take_info),
    path('sen_info_tp_hm', views.API_info_tp_hm),
    path('sen_info_wlvl', views.API_info_wlvl),
    path('delete_sen', views.API_delete_sen),
    path('dashsen_all', views.API_dashsen_all),

    #path('sen_info_capacidad', views.API_info_riego),
]