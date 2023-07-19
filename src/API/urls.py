from django.urls import path
from .views import RoomView, CreateRoomView, GetRoomView, JoinRoomView, InRoomCheck, LeaveRoom, EditRoom
urlpatterns = [
    path('', RoomView.as_view(), name='all-rooms'),
    path('create-room/', CreateRoomView.as_view(), name='create-room'),
    path('room/', GetRoomView.as_view(), name='room'),
    path('join/', JoinRoomView.as_view(), name='join-room'),
    path('in-room/', InRoomCheck.as_view(), name='check-in-room'),
    path('leave/', LeaveRoom.as_view(), name='leave-room'),
    path('update/', EditRoom.as_view(), name='update-room'),
]
