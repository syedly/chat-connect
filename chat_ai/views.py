from django.shortcuts import render, HttpResponse
from .openai_utils import get_openai_response
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
# Create your views here.

@csrf_exempt
def chat_ai(request):
    response = ""
    if request.method == 'POST':
        user_input = request.POST.get('user_input', '').strip()
        if user_input:
            try:
                response = get_openai_response(user_input)
            except Exception as e:
                response = f"Error: {str(e)}"
        else:
            response = "No input provided."

        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'message': response})

    return render(request, 'chat_ai.html', {'response': response})