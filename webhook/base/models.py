from django.db import models


# Create your models here.
from webhook import settings


class Register(models.Model):
    nickname = models.CharField(max_length=128, )
    date = models.DateField()
    time = models.TimeField()
    player_id = models.IntegerField()
    media_id = models.IntegerField()
    media_type = models.CharField(max_length=2, )

    class Meta:
        unique_together = ('date', 'time', 'player_id',)

    def __str__(self):
        return f"{self.player_id} {self.date} - {self.time} - {self.media_id}"


class Account(models.Model):
    name = models.CharField(max_length=128, primary_key=True, )
    register = models.ManyToManyField(Register, blank=True)

    def __str__(self):
        return f"{self.name}"
