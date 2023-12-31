from django.db import models

class SpotifyTokens(models.Model):
    host = models.CharField(max_length=50, unique=True)
    access_token = models.CharField(max_length=150)
    refresh_token = models.CharField(max_length=150)
    token_type = models.CharField(max_length=50)
    expires_in = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)