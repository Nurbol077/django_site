from django.shortcuts import render



def kino(request):
    return render(request, 'kino.html')