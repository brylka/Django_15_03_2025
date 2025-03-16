from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404

from .forms import LinearEquationForm, PostForm


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
    # if request.GET.get('sort'):
    sort = request.GET.get('sort', 'id')
    # else:
    #     sort = 'id'
    posts = Post.objects.all().order_by(sort)
    return render(request, 'myapp/table.html', {'posts': posts})


def create_post(request):
    form = PostForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
            form.save()
            return redirect("post_list")

    return render(request, "myapp/post_form.html", {"form": form, "title": "Dodaj post"})
    # if request.method == 'POST':
    #     title = request.POST.get('title')
    #     content = request.POST.get('content')
    #     if title and content:
    #         Post.objects.create(title=title, content=content)
    #         return redirect("post_list")
    #     else:
    #         return HttpResponse("Tytuł i treść są wymagane!")
    #
    # return render(request, 'myapp/create_post.html')


def update_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    form = PostForm(request.POST or None, instance=post)

    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("post_list")

    return render(request, "myapp/post_form.html",
                  {"form": form, "title": "Edytuj post"})

    # post = get_object_or_404(Post, id=post_id)
    #
    # if request.method == 'POST':
    #     if request.POST.get('_method') == "PUT":
    #         if request.POST.get('title') and request.POST.get('content'):
    #             post.title = request.POST.get('title')
    #             post.content = request.POST.get('content')
    #             post.save()
    #             return redirect("post_list")
    #         else:
    #             return HttpResponse("Tytuł i treść są wymagane!")
    #
    # return render(request, 'myapp/update_post.html', {"post": post})


def delete_post(request, post_id):
    print("ala")
    post = get_object_or_404(Post, id=post_id)

    if request.method == "DELETE":
        post.delete()
        return JsonResponse({"message": "Post usunięty"}, status=204)

    return JsonResponse({"error": "Metoda niedozwolona"}, status=405)


def zero_point(request):
    x0 = None
    if request.method == 'POST':
        form = LinearEquationForm(request.POST)
        if form.is_valid():
            a = form.cleaned_data['a']
            b = form.cleaned_data['b']

            if a != 0:
                x0 = -b / a
            else:
                x0 = 'Brak miejsc zerowych.'
    else:
        form = LinearEquationForm()
    return render(request, "myapp/zero_point.html", {"form": form, "x0": x0})