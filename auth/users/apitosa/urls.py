from django.urls import path
from . import views


urlpatterns = [
    path('show', views.get_in),
    path('show_hours',views.get_in_hour),
    path('get_data_op',views.get_data_op),
    path('save_data_op',views.save_data_op),
    path('register_new_hour',views.hour_view_register),
    path('delete_hour/<id>',views.delete_hourss.as_view()),
    path('add_space', views.API_add_space),
    path('get_spaces', views.API_get_spaces),
    #path('show', views.get_Info)
    #infodb

]
