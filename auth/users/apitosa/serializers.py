from rest_framework.serializers import ModelSerializer
#from auth.users.models import show_info
from ..models import *



class show_info_serializer(ModelSerializer):
    class Meta:
        model = show_info
        fields = '__all__'

class register_hour_serializer(ModelSerializer):
    class Meta:
        model = Register_new_hour
        fields = '__all__'

class save_op(ModelSerializer):
    class Meta:
        model = Save_opcion
        fields = '__all__'




class new_space(ModelSerializer):
    class Meta:
        model = NewSpace
        fields = '__all__'