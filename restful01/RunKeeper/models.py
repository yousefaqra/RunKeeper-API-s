from django.contrib.auth.models import User
from django.db import models
from django.db.models import Avg, Sum


# Create your models here.


class Session(models.Model):

    distance_in_miles = models.FloatField()
    length_of_run = models.FloatField()
    owner = models.ForeignKey(
        'auth.User',
        related_name='Session',
        on_delete=models.CASCADE)

    class Meta:
        ordering = ('-distance_in_miles',)
