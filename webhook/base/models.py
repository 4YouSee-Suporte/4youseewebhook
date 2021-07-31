from django.db import models


class Account(models.Model):
    name = models.CharField(max_length=128, primary_key=True, )
    url = models.CharField(max_length=100, blank=True, default="-")

    def __str__(self):
        return f"{self.name}"

class Register(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='records')
    nickname = models.CharField(max_length=128, )
    date = models.DateField()
    time = models.TimeField()
    player_id = models.IntegerField()
    media_id = models.IntegerField()
    media_type = models.CharField(max_length=2, )

    class Meta:
        unique_together = ('date', 'time', 'player_id',)
        ordering = ['date', 'time']

    def __str__(self):
        return f"{self.player_id} {self.date} - {self.time} - {self.media_id}"
