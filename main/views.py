from django.shortcuts import render


def phones(request):
    return render(phones, 'phomes.html')
# Create your views here.

def book_list(request):
    return render(request, 'book.html')

