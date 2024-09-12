from django.urls import path
from . import views

urlpatterns = [
    path('', views.chat_ai, name="chat_ai"),

]