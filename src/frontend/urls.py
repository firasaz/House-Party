from django.urls import path, re_path
from .views import index

app_name = 'frontend'
urlpatterns = [
    # re_path('.*', index),
    path('', index, name='index'),
    path('create-room/', index),
    path('room/<str:roomCode>/', index),
    path('join/', index),
]