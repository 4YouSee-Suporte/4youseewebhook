from django.db import models


class Client(models.Model):
    name = models.CharField(max_length=128)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name}"


class Register(models.Model):
    account = models.ForeignKey("manager.Account", on_delete=models.CASCADE, related_name='records')
    nickname = models.CharField(max_length=128)
    date = models.DateField()
    time = models.TimeField()
    player_id = models.IntegerField()
    media_id = models.IntegerField()
    media_type = models.CharField(max_length=2)

    class Meta:
        unique_together = ('date', 'time', 'player_id', 'nickname')
        ordering = ['date', 'time']

    def __str__(self):
        return f"{self.player_id} {self.player_id} {self.date} - {self.time} - {self.media_id}"
