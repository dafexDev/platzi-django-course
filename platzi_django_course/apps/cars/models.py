from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
import datetime


class Car(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255)
    year = models.PositiveIntegerField(
        validators=[
            MinValueValidator(1886), # First car year
            MaxValueValidator(datetime.date.today().year),
        ],
        null=True,
        blank=True
    )
