from django.urls import path

from checker_channel import consumers

websocket_urlpatterns = [
    path('ws/checker_channel/<str:room_name>/', consumers.CheckerChannelConsumer),
]
