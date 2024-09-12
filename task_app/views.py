from django.shortcuts import render, get_object_or_404
from .forms import CustomUserCreationForm
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, DeleteView
from django.contrib.auth.models import User
from .models import Message
from django.db.models import Q
from django.core.paginator import Paginator
from django.http import JsonResponse

def index(request):
    return render(request, 'index.html')

class SignupView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'signup.html'
    success_url = reverse_lazy('login')

class HomeListView(ListView):
    model = User
    template_name = 'home.html'
    context_object_name = 'users'
    paginate_by = 3

class ChatView(DetailView):
    model = User
    template_name = 'chat.html'
    context_object_name = 'recipient'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        recipient = self.get_object()
        current_user = self.request.user

        context['recipient'] = recipient

        context['messages'] = Message.objects.filter(
            (Q(sender=current_user) & Q(recipient=recipient)) |
            (Q(sender=recipient) & Q(recipient=current_user))
        ).order_by('timestamp')

        return context

class DeleteMessageView(DeleteView):
    model = Message

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()

        # Check for AJAX request
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'message': 'Message deleted successfully'}, status=200)

        return super().delete(request, *args, **kwargs)