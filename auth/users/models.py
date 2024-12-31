from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
 #hora 1:50:25
class User(AbstractUser):
    name = models.CharField(max_length=8)
    username = models.CharField(unique=True, max_length=10)
    password = models.CharField(max_length=20)
    email = models.CharField(unique=True,max_length=35)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']


class show_info(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField()

class Save_opcion(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # Un campo de tipo JSONField para almacenar datos en formato JSON
    json = models.JSONField(unique=True)


class sen_temp_agua(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # Un campo de tipo JSONField para almacenar datos en formato JSON
    json = models.JSONField()



class Register_new_hour(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50,unique=True)
    cual_ench = models.CharField(max_length=50, unique=True)
    hour_on = models.IntegerField()
    hour_off = models.IntegerField()
    status = models.CharField(max_length=1)
    joint_hour = models.BooleanField(default=True) #para poder tener horario de crecimiento y flora enlazao a 1 solo ;)
    use_hour = models.BooleanField(default=True)

    def __str__(self):
        texto = "{0} ({1})"
        return texto.format(self.name,self.hour_on,self.hour_off,self.status)

class Register_new_enchufe(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50,unique=True)
    numero_enchufe = models.IntegerField()
    estado = models.CharField(max_length=9)

    def __str__(self):
        texto = "{0} ({1})"
        return texto.format(self.user,self.name,self.numero_enchufe,self.estado)



class NewSpace(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cat_space = models.PositiveIntegerField(primary_key=True, unique=True, editable=False)
    nombre = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # Si es un nuevo objeto, asigna el valor para cat_space automáticamente
        if not self.pk:
            last_cat_space = NewSpace.objects.order_by('-cat_space').first()
            self.cat_space = 1 if not last_cat_space else last_cat_space.cat_space + 1
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nombre



