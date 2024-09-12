from django.urls import re_path
from task_app.consumers import ChatConsumer

websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<recipient_pk>\d+)/$', ChatConsumer.as_asgi()),
]
