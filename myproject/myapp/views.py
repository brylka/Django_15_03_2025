from django.http import HttpResponse
from django.shortcuts import render, redirect


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


def create_post(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        if title and content:
            Post.objects.create(title=title, content=content)
            return redirect("post_list")
        else:
            return HttpResponse("Tytuł i treść są wymagane!")

    return render(request, 'myapp/create_post.html')


def update_post(request, post_id):
    pass