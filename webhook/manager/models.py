from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.urls import reverse


class Account(models.Model):
    name = models.CharField(max_length=128, unique=True)
    url = models.CharField(max_length=100, unique=True)
    token = models.CharField(max_length=100)
    slug = models.SlugField(null=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name}"

    def get_absolute_url(self):
        return reverse('manager:conta', kwargs={'slug': self.slug})

    class Meta:
        ordering = ['-date_added']


class Playlist(models.Model):
    playlist_id = models.IntegerField()
    name = models.CharField(max_length=128)
    isSubPlaylist = models.BooleanField()
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='playlists')

    def __str__(self):
        return f"{self.playlist_id} - {self.name}"


class Player(models.Model):
    player_id = models.IntegerField()
    name = models.CharField(max_length=128)
    platform = models.CharField(max_length=28)
    lastContactInMinutes = models.IntegerField(null=True)
    group_id = models.IntegerField()
    group_name = models.CharField(max_length=128)
    status_id = models.IntegerField()
    status_name = models.CharField(max_length=128)
    lastLogReceived = models.DateTimeField(null=True)
    playlist = models.ForeignKey(Playlist, on_delete=models.SET_NULL, null=True, related_name='players')
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='players')

    def __str__(self):
        return f"{self.player_id} - {self.name}"


class Category(models.Model):
    category_id = models.IntegerField()
    name = models.CharField(max_length=64)
    description = models.CharField(max_length=128)
    autoShuffle = models.BooleanField()
    updateflow = models.IntegerField()
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='categories')

    def __str__(self):
        return f"{self.category_id} - {self.name}"


class Media(models.Model):
    media_id = models.IntegerField()
    name = models.CharField(max_length=128)
    file = models.CharField(max_length=13)
    durationInSeconds = models.IntegerField()
    startDate = models.DateField(blank=True, null=True)
    endDate = models.DateField(blank=True, null=True)
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='medias')
    category = models.ManyToManyField(Category, related_name='medias')
    playlist = models.ManyToManyField(Playlist, related_name='medias')
    client = models.ForeignKey("base.Client", blank=True, null=True, on_delete=models.SET_NULL, related_name='medias')

    def __str__(self):
        return f"{self.media_id} - {self.name}"
