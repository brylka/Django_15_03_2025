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

def divide(request, a, b):
    if b != 0:
        c = a / b
    else:
        c = None
    return render(request,
                  'myapp/divide.html',
                  {'a': a, 'b': b, 'c': c})


def table(request):
    posts = [
        {"id": 1, "title": "Pierwszy post", "content": "Treść pierwszego posta", "create_at": "2025-03-01"},
        {"id": 2, "title": "Drugi post", "content": "Treść drugiego posta", "create_at": "2025-03-05"},
        {"id": 3, "title": "Trzeci post", "content": "Treść trzeciego posta", "create_at": "2025-03-15"},
        {"id": 4, "title": "Czwarty post", "content": "Treść czwartego posta", "create_at": "2025-03-15"},
    ]
    #posts = []

    # for post in posts:
    #     print(f"Lp. {post['id']}, Tytuł: {post['title']}, Treść: {post['content']}, Data {post['create_at']}")

    return render(request, 'myapp/table.html', {'posts': posts})


from .models import Post
def post_list(request):
    posts = Post.objects.all()
    return render(request, 'myapp/table.html', {'posts': posts})