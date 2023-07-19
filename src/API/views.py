from django.shortcuts import render
from rest_framework import generics, status
from .models import Room
from .serializers import RoomSerializer, CreateRoomSerialzier
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import JsonResponse

# Create your views here.
class RoomView(generics.ListCreateAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

class CreateRoomView(APIView):
    serializer_class = CreateRoomSerialzier
    def post(self, request, format=None):
        if not self.request.session.exists(self.request.session.session_key):
            self.request.session.create()
        
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            # guests_pause, votes_to_skip = serializer.data
            guests_pause = serializer.data.get('guests_pause')
            votes_to_skip = serializer.data.get('votes_to_skip')
            user_id = self.request.session.session_key
            queryset = Room.objects.filter(host=user_id)
            if queryset.exists():
                room = queryset[0]
                room.guests_pause = guests_pause
                room.votes_to_skip = votes_to_skip
                room.save(update_fields=['guests_pause', 'votes_to_skip'])
            else:
                room = Room(host=user_id, guests_pause=guests_pause, votes_to_skip=votes_to_skip)
                room.save()
            
            self.request.session['room_code'] = room.code
            return Response(RoomSerializer(room).data, status=status.HTTP_201_CREATED)
        return Response({'Bad Request': 'Invalid data...'}, status=status.HTTP_400_BAD_REQUEST)

class GetRoomView(APIView):
    serializer_class = RoomSerializer
    lookup_url_kwarg = 'code'

    def get(self, request, format=None):
        code = request.GET.get(self.lookup_url_kwarg) # this is to "get" the word "code" from the url in request.GET
        if code:
            room = Room.objects.filter(code=code) # returns a queryset of all rooms with code code which should be only 1 room since code is unique
            if len(room) == 1:
                serializer = RoomSerializer(room[0]) # serialized data
                room_data = serializer.data # extract the data and store it in a room_data
                room_data['is_host'] = self.request.session.session_key == room[0].host # add a new key to the data that stores True if the request's session key equals the founded room's host value otherwise False
                return Response(room_data, status=status.HTTP_200_OK)
            return Response({"Room Not Found": "Invalid Room Code"}, status=status.HTTP_404_NOT_FOUND)
        return Response({"Bad Request": "Code Not Given"}, status=status.HTTP_400_BAD_REQUEST)

class JoinRoomView(APIView):
    lookup_url_kwarg = 'code'
    def post(self, request, format=None):
        if not self.request.session.exists(self.request.session.session_key):
            self.request.session.create()
        print(self.request.session.session_key)
        code = request.data.get(self.lookup_url_kwarg)
        print(code)
        if code != None:
            queryset = Room.objects.filter(code=code)
            if queryset.exists():
                room = queryset[0]
                self.request.session['room_code'] = code
                return Response({'Message': 'Room Joined Successfully!'}, status=status.HTTP_200_OK)
            return Response({'Bad Request': 'Invalid Room Code'}, status=status.HTTP_404_NOT_FOUND)
        return Response({'Bad Request': 'Room Code Not Given'}, status=status.HTTP_400_BAD_REQUEST)

class InRoomCheck(APIView):
    def get(self, request, format=None):
        if not self.request.session.exists(self.request.session.session_key):
            self.request.session.create()
        code = self.request.session.get('room_code')
        return JsonResponse(
            {
                'room_code': code
            }, status=status.HTTP_200_OK)

class LeaveRoom(APIView):
    def get(self, request, format=None):
        code = self.request.session.pop('room_code')
        host = self.request.session.session_key
        room = Room.objects.filter(code=code)
        if room:
            room = room[0]
            if room.host == host:
                room.delete()
            return Response({'Message': 'Left Room Successfully'}, status=status.HTTP_200_OK)
        return Response({'Bad Request': 'Invalid Room Code Given'}, status=status.HTTP_400_BAD_REQUEST)

class EditRoom(APIView):
    serializer_class = CreateRoomSerialzier
    def patch(self, request, format=None):
        if not self.request.session.exists(self.request.session.session_key):
            self.request.session.create()
        
        room_code = self.request.session.get('room_code') # get the "room_code" value stored in the user's previous session. if None, user never joined or created a room thus is definitely not a host so no room will be found and the attempt to edit the room will fail
        serializer = self.serializer_class(data=request.data) # serialize the request to extract the only 2 options we need to modify which are "votes_to_skip" and "guests_can_pause"
        if serializer.is_valid():
            guests_pause = serializer.data.get('guests_pause') # "guest_can_pause" is a key in json in the serialized data
            votes_to_skip = serializer.data.get('votes_to_skip') # "votes_to_skip" is a key in json in the serialized data
            queryset = Room.objects.filter(code=room_code) # returns a queryset
            if queryset.exists():
                room = queryset[0]
                user_id = self.request.session.session_key
                if room.host == user_id:
                    room.guests_pause = guests_pause
                    room.votes_to_skip = votes_to_skip
                    room.save(update_fields=['guests_pause','votes_to_skip'])
                    return Response(RoomSerializer(room).data, status=status.HTTP_200_OK)
                return Response({'Error': 'You are not the host of this room!'}, status=status.HTTP_403_FORBIDDEN)
            return Response({'Error': 'Room Not Found.'}, status=status.HTTP_404_NOT_FOUND)
        return Response({'Bad Request': 'Invalid Data'}, status=status.HTTP_400_BAD_REQUEST)