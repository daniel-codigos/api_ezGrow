from rest_framework.serializers import ModelSerializer
#from auth.users.models import show_info
from .models import *


class save_info_meross(ModelSerializer):
    class Meta:
        model = SaveMerossInfo
        fields = '__all__'



class save_enchufes_data(ModelSerializer):
    class Meta:
        model = SaveEnchuData
        fields = '__all__'


class save_aparato_data(ModelSerializer):
    class Meta:
        model = SaveAparatoData
        fields = '__all__'


class save_hora(ModelSerializer):
    class Meta:
        model = SaveHora
        fields = '__all__'

class save_riego(ModelSerializer):
    class Meta:
        model = SaveRiego
        fields = '__all__'

class save_bidones(ModelSerializer):
    class Meta:
        model = SaveBidones
        fields = '__all__'

class save_lanzar_riego(ModelSerializer):
    class Meta:
        model = SaveLanzarRiego
        fields = '__all__'



class todas_rutinas(ModelSerializer):
    class Meta:
        model = TodasRutinas
        fields = '__all__'

class save_rellena(ModelSerializer):
    class Meta:
        model = SaveInfoRelleno
        fields = '__all__'

class save_old_culti(ModelSerializer):
    class Meta:
        model = SaveOldCulti
        fields = '__all__'