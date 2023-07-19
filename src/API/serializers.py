from rest_framework import serializers
from .models import Room
from spotify.models import SpotifyTokens

class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = '__all__'

class CreateRoomSerialzier(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ['guests_pause', 'votes_to_skip']

class TokensSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpotifyTokens
        fields = '__all__'