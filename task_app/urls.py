from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import SignupView, HomeListView, ChatView, DeleteMessageView
from .views import index

urlpatterns = [
    path('', index, name='index'),
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('signup/', SignupView.as_view(), name='signup'),
    path('home/', HomeListView.as_view(), name='home'),
    path('chat-user/<int:pk>/', ChatView.as_view(), name='chat-user'),
    path('delete-message/<int:pk>', DeleteMessageView.as_view(), name='delete-message')
]
