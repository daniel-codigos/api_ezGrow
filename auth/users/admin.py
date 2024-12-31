from django.contrib import admin

# Register your models here.
from .models import *
#Show_infos

admin.site.register(User)
admin.site.register(show_info)
admin.site.register(Register_new_hour)
admin.site.register(Save_opcion)

