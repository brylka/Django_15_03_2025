from django.http import HttpResponse
from django.shortcuts import render


def hello_world(request):
    #return HttpResponse("Hello, World!")
    return render(request, 'myapp/hello_world.html')


def hello_name(request, name):
    #return HttpResponse(f"Hello, {name}!")
    return render(request,
                  'myapp/hello_name.html',
                  {'name': name, 'klucz': 'wartość'})


def add(request, a, b):
    result = a + b
    #return HttpResponse(f"{a} + {b} = {result}")
    return render(request,
                  'myapp/add.html',
                  {'a': a, 'b': b, 'c': result})
