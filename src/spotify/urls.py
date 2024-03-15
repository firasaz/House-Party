from django.urls import path
from .views import *

app_name = 'spotify'
urlpatterns = [
    path('get-auth-url/', AuthUrl.as_view()),
    path('redirect/', spotify_callback),
    path('is-authenticated/', IsAuthenticated.as_view()),
    path('current-song/', CurrentSong.as_view()),
    path('control/', PlaySong.as_view()),
    path('delete-token/', delete_tokens),
    path('tokens/', tokens_db),

    path('play/', PlaySong.as_view()),
    path('pause/', PauseSong.as_view())
]