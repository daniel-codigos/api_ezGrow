from django.db import models
from django.contrib.auth.models import AbstractUser
from ..models import User
from djongo import models as modelsjongo

class SaveMerossInfo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    email = models.CharField(max_length=100)
    passwd = models.CharField(max_length=100)
    info = models.JSONField()
    timestamp = models.DateTimeField(auto_now_add=True)
    space = models.CharField(max_length=25)
    #info = models.JSONField()

    def __str__(self):
        return f"Email: {self.email}, User: {self.user}, pass: {self.passwd}, space: {self.space}, info:{self.info}"

class SaveEnchuData(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    info = models.JSONField()
    timestamp = models.DateTimeField(auto_now_add=True)
    #info = models.JSONField()

    def __str__(self):
        return f"User: {self.user}, info: {self.info}"


class SaveAparatoData(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    info = models.JSONField()
    timestamp = models.DateTimeField(auto_now_add=True)
    #info = models.JSONField()

    def __str__(self):
        return f"user_id: {self.user.id}, info: {self.info}, timestamp: {self.timestamp}"


class SaveHora(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    info = models.JSONField()
    timestamp = models.DateTimeField(auto_now_add=True)
    #info = models.JSONField()

    def __str__(self):
        return f"User: {self.user}, info: {self.info}"

class SaveRiego(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    info = models.JSONField()
    timestamp = models.DateTimeField(auto_now_add=True)
    #info = models.JSONField()

    def __str__(self):
        return f"User: {self.user}, info: {self.info}"

class SaveBidones(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    info = models.JSONField()
    timestamp = models.DateTimeField(auto_now_add=True)
    #info = models.JSONField()

    def __str__(self):
        return f"User: {self.user}, info: {self.info}"

class SaveLanzarRiego(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    info_riego = models.JSONField()
    timestamp = models.DateTimeField(auto_now_add=True)
    #info = models.JSONField()

    def __str__(self):
        return f"User: {self.user}, info: {self.info_riego}"


class SaveInfoRelleno(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    info_relleno = models.JSONField()
    timestamp = models.DateTimeField(auto_now_add=True)
    #info = models.JSONField()

    def __str__(self):
        return f"User: {self.user}, info: {self.info_relleno}"

class TodasRutinas(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    info = models.JSONField()
    #info = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    #info = models.JSONField()

    def __str__(self):
        return f"User: {self.user}, info: {self.info}"


class SaveOldCulti(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    info = models.JSONField()
    timestamp = models.DateTimeField(auto_now_add=True)
    #info = models.JSONField()

    def __str__(self):
        return f"User: {self.user}, info: {self.info}"
