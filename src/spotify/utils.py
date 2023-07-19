from django.utils import timezone
from datetime import timedelta
from requests import post, put, get
from rest_framework.response import Response

from .models import SpotifyTokens
import os
from dotenv import load_dotenv

load_dotenv()

BASE_URL = 'https://api.spotify.com/v1/me/'

# Get Host Tokens
def get_user_tokens(session_key):
    user_tokens = SpotifyTokens.objects.filter(host=session_key) # check whether an existing tokens object is found
    return user_tokens[0] if user_tokens.exists() else None # returns a SpotifyTokens object | None

# Update Existing or Save Host Tokens in Database
def create_or_update_user_tokens(session_key, access_token, token_type, expires_in, refresh_token=None):
    print(expires_in)
    tokens_obj = get_user_tokens(session_key)
    expires_in = timezone.now() + timedelta(seconds=expires_in)

    if tokens_obj: # if an existing object is found, then we need to update the expired tokens
        tokens_obj.access_token = access_token
        # tokens_obj.refresh_token = refresh_token # spotify doesn't update refresh_token so we won't update it
        tokens_obj.token_type = token_type
        tokens_obj.expires_in = expires_in
        tokens_obj.save(update_fields=['access_token', 'token_type', 'expires_in'])
    else: # else this is the first time we're creating an object for the host and their tokens
        tokens_obj = SpotifyTokens(host=session_key, access_token=access_token, refresh_token=refresh_token, token_type=token_type, expires_in=expires_in)
        tokens_obj.save()

# Checking User Authentication Status
def is_spotify_authenticated(session_key):
    tokens_obj = get_user_tokens(session_key) # returns a SpotifyTokens object
    print(tokens_obj)
    if tokens_obj: # if the user is saved in the database, that means he was authenticated at some point and he has/had a valid token
        expiry = tokens_obj.expires_in
        print(f'Token Expiry: {expiry}')
        print(f'Time Now: {timezone.now()}')
        if expiry <= timezone.now(): # here we check if the token is expired or not
            refresh_spotify_token(session_key, tokens_obj.refresh_token) # if token is expired, call the 'refresh_spotify_token' to get new tokens without authenticating with the user again
        print(True)
        return True
    return False

# Retrieve New Tokens When Old Ones Expire
def refresh_spotify_token(session_key, refresh_token):
    response = post('https://accounts.spotify.com/api/token', data={
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token,
        'client_id': os.getenv('CLIENT_ID'),
        'client_secret': os.getenv('CLIENT_SECRET'),
    }).json()

    print(response)
    access_token = response.get('access_token')
    # refresh_token = response.get('refresh_token') # this is returning null since spotify doesn't update the refresh_token instead we resuse the existing token
    token_type = response.get('token_type')
    expires_in = response.get('expires_in')

    create_or_update_user_tokens(session_key, access_token, token_type, expires_in) # update the database with the new tokens

def spotify_api_requests(session_key, endpoint, _post=None, _put=None):
    tokens_obj = get_user_tokens(session_key)
    if not tokens_obj:
        return {'Bad Request': "Host doesn't have authentication tokens"}
    # is_spotify_authenticated(session_key) # not sure if this is necessary
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {tokens_obj.access_token}'
    }

    if _post:
        post(BASE_URL + endpoint, headers=headers)
    if _put:
        print('spotify "PUT" request')
        response=put(BASE_URL + endpoint, headers=headers)
        print(response.json())

    response = get(BASE_URL + endpoint, {}, headers=headers)
    try:
        return response.json()
    except:
        print("couldn't find current song")
        return {'error': {'message': 'Issue With Request', 'check': 'Make Sure Spotify is Open'}} # Response object from rest_framework.response cannot be used here as this is not a class inheriting from APIView nor the api_view decorator is places on the function
    
def play_song(session_key):
    print('play')
    return spotify_api_requests(session_key, 'player/play/', _put=True)
    
def pause_song(session_key):
    print('pause')
    return spotify_api_requests(session_key, 'player/pause/', _put=True)
