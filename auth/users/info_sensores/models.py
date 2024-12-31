from django.db import models
from django.contrib.auth.models import AbstractUser
from ..models import User


class InfoSenWLevel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True)
    info = models.JSONField()

    def __str__(self):
        return self.name

class InfoSenTpHm(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    space_name = models.CharField(max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True)
    info = models.JSONField()

    def __str__(self):
        return self.name


class SaveNewSenInfo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    info = models.JSONField()
    timestamp = models.DateTimeField(auto_now_add=True)
    #info = models.JSONField()

    def __str__(self):
        return f"Info de usuario: {self.user}, Fecha: {self.timestamp}, info: {self.info}"

class InfoSensor(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    space_name = models.CharField(max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True)
    info = models.JSONField()

    def __str__(self):
        return self.name
