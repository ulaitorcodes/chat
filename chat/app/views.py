from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def lobby(request):
    template_name = 'chat/lobby.html'
    context = dict({

    })

    return render (request, template_name, context)