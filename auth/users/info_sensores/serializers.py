from rest_framework.serializers import ModelSerializer
#from auth.users.models import show_info
from .models import *



class save_info_sen_wlvl(ModelSerializer):
    class Meta:
        model = InfoSenWLevel
        fields = '__all__'


class save_info_sen_tp_hm(ModelSerializer):
    class Meta:
        model = InfoSenTpHm
        fields = '__all__'


class save_new_info(ModelSerializer):
    class Meta:
        model = SaveNewSenInfo
        fields = '__all__'

class info_sensor(ModelSerializer):
    class Meta:
        model = InfoSensor
        fields = '__all__'
