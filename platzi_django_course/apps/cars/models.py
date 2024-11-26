from django.db import models


class Car(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255)
