from django.shortcuts import render


# Create your views here.

def home_frontend(request):
    return render(request, 'app/home.html')
