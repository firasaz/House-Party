from django.shortcuts import redirect
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from requests import Request, post

from API.serializers import TokensSerializer
from .models import SpotifyTokens
from django.http import JsonResponse
from .utils import create_or_update_user_tokens, is_spotify_authenticated, spotify_api_requests, play_song, pause_song, get_user_tokens
from API.models import Room

import os
from dotenv import load_dotenv

load_dotenv()

# Connecting and Authenticating With Spotify API
class AuthUrl(APIView):
    def get(self, request, format=None):
        scopes = 'user-read-playback-state user-modify-playback-state user-read-currently-playing'
        # print(os.getenv('REDIRECT_URI'))

        # the following generates the URL that sends a request to spotify to access permissions specified in the 
        # 'scopes' above which spotify then displays a window to the user informing him of myh application's 
        # request to access the permissions
        url = Request('GET', 'https://accounts.spotify.com/authorize', params={
            'scope': scopes,
            'response_type': 'code',
            'redirect_uri': os.getenv('REDIRECT_URI'),
            'client_id': os.getenv('CLIENT_ID')
        }).prepare().url

        return Response({'url': url}, status=status.HTTP_200_OK)

# Creating the Authentication Tokens
def spotify_callback(request, format=None):
    code = request.GET.get('code')
    error = request.GET.get('error') # if there is an error in the request

    # the 'response' here is spotify's response after we send a POST request to get the required tokens
    # that we need to access the user's info which he/she just gave us permission and spotify returned the 
    # 'code' value to us and using that code we request the access token
    response = post('https://accounts.spotify.com/api/token', data={
        'grant_type': 'authorization_code',
        'code': code,
        'client_id': os.getenv('CLIENT_ID'),
        'client_secret': os.getenv('CLIENT_SECRET'),
        'redirect_uri': os.getenv('REDIRECT_URI')
    }).json()
    # print(response)
    if 'error' in response or 'access_token' not in response:
        # print(response)
        return JsonResponse(response)

    access_token = response.get('access_token')
    refresh_token = response.get('refresh_token')
    token_type = response.get('token_type')
    expires_in = response.get('expires_in')
    error = response.get('error')

    if not request.session.exists(request.session.session_key):
        request.session.create()

    create_or_update_user_tokens(request.session.session_key, access_token, token_type, expires_in, refresh_token)
    return redirect('frontend:index')

class IsAuthenticated(APIView):
    def get(self, request):
        is_authenticated = is_spotify_authenticated(self.request.session.session_key)
        # print(is_authenticated)
        return Response({'status': is_authenticated}, status=status.HTTP_200_OK)

class CurrentSong(APIView):
    def get(self, request):
        room_code = self.request.session.get('room_code') # from vite server, "room_code" is None thus room is not found
        queryset = Room.objects.filter(code = room_code)
        if not queryset.exists():
            return Response({'Error': 'Room Not Found'}, status=status.HTTP_404_NOT_FOUND)
        room = queryset[0]
        host = room.host
        endpoint = 'player/currently-playing/'

        response = spotify_api_requests(host, endpoint) # returns data in json format
        if 'error' in response or 'item' not in response:
            return Response(response, status=status.HTTP_401_UNAUTHORIZED)
        item = response.get('item')
        song_id = response.get('id')
        duration = item.get('duration_ms')
        progress = response.get('progress_ms')
        album_cover = {
            'big_img': item.get('album').get('images')[0], 
            'med_img': item.get('album').get('images')[1],
            'sm_img': item.get('album').get('images')[2]
            }
        is_playing = response.get('is_playing')

        artists = ''
        for i, artist in enumerate(item.get('artists')):
            if i>0:
                artists += ', ' # after the 1st name, we add a comma and a space to separate the rest of the artists
            artists += artist.get('name')
        
        song_data = {
            'title': item.get('name'),
            'artist': artists,
            'duration_ms': duration,
            'timestamp_ms': progress,
            'images_urls': album_cover,
            'is_playing': is_playing,
            'id': song_id
        }
        return Response(song_data, status=status.HTTP_200_OK)

class PlaySong(APIView):
    def put(self, request):
        code = self.request.session.get('room_code')
        control = request.data.get('control')
        queryset = Room.objects.filter(code=code)
        if not queryset.exists():
            return Response({'Error': 'Room Not Found'}, status=status.HTTP_404_NOT_FOUND)
        room = queryset[0]
        #check if user can play or pause song or if they are the host
        if self.request.session.session_key == room.host or room.guests_pause:
            play_song(room.host) if control == 'play' else pause_song(room.host)
            return Response({}, status=status.HTTP_204_NO_CONTENT)
        return Response({}, status=status.HTTP_403_FORBIDDEN)

@api_view(['DELETE'])
def delete_tokens(request):
    session_key = request.session.session_key
    tokens_obj = get_user_tokens(session_key)
    if tokens_obj:
        tokens_obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def tokens_db(request):
    tokens = SpotifyTokens.objects.all()
    serializer = TokensSerializer(tokens, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

class PlaySong(APIView):
    def put(self, response, format=None):
        room_code = self.request.session.get('room_code')
        room = Room.objects.filter(code=room_code)[0]
        if self.request.session.session_key == room.host or room.guest_can_pause:
            play_song(room.host)
            return Response({}, status=status.HTTP_204_NO_CONTENT)

        return Response(response['error'], status=status.HTTP_403_FORBIDDEN)

class PauseSong(APIView):
    def put(self, response, format=None):
        room_code = self.request.session.get('room_code')
        room = Room.objects.filter(code=room_code)[0]
        if self.request.session.session_key == room.host or room.guest_can_pause:
            response = pause_song(room.host)
            return Response(response['error'], status=status.HTTP_204_NO_CONTENT)
            
        return Response(response['error'], status=status.HTTP_403_FORBIDDEN)