import json

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from openai import OpenAI

from .forms import LinearEquationForm, PostForm, ChatForm


def hello_world(request):
    return render(request, 'myapp/hello_world.html')


def hello_name(request, name):
    return render(request,
                  'myapp/hello_name.html',
                  {'name': name, 'klucz': 'wartość'})


def add(request, a, b):
    result = a + b
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

    return render(request, 'myapp/table.html', {'posts': posts})


from .models import Post
def post_list(request):
    sort = request.GET.get('sort', 'id')
    posts = Post.objects.all().order_by(sort)
    return render(request, 'myapp/table.html', {'posts': posts})


def create_post(request):
    form = PostForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
            form.save()
            return redirect("post_list")

    return render(request, "myapp/post_form.html",
                  {"form": form, "title": "Dodaj post"})


def update_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    form = PostForm(request.POST or None, instance=post)

    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("post_list")

    return render(request, "myapp/post_form.html",
                  {"form": form, "title": "Edytuj post"})


def delete_post(request, post_id):
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


def get_api_key():
    """Pobiera klucz API z pliku openai_key.txt"""
    try:
        with open('../openai_key.txt', 'r') as f:
            return f.read().strip()
    except FileNotFoundError:
        print("Błąd: Plik openai_key.txt nie został znaleziony.")
        return None
    except Exception as e:
        print(f"Błąd odczytu pliku z kluczem API: {str(e)}")
        return None

def chat(request):
    preprompt = """Jesteś asystentem mojej firmy Bartosz Company. Masz za zadanie odpowiadać klientom na temat naszych produktów.
    FIRMA ZAJMUJE SIĘ:
    1. Tylko i wyłącznie sprzedaż systemów: Windows 11, Linux Debian 13
    2. Tylko i wyłącznie sprzedaż oprogramowania biurowego: MS Office 365
    3. Niczym poza tym nie handlujemy i nie doradzamy
    
    DORADZAJ klientowi zakup TYLKO naszych produktów! 
    NIE proponuj innych. Sprzedajemy tylko nasze.
    
    WAŻNE:
    1. Jak klient zapyta o produkt innym niż nasz (nawet kuchenkę mikrofalową), zaproponuj, że potrezbuje do tego system operacyjny, który sprzedajemy.
    2. Zachwalaj nasze usługi!
    3. Na dzień dobry przedstaw naszą oefrtę, niezależnie co chce klient.
    
    Tu jest pierwsze pytanie klienta:
    """
    messages = []
    api_key = get_api_key()
    error_message = None
    model = "gpt-3.5-turbo"
    assistant_response = None
    response = None

    if not api_key:
        error_message = "Błędna konfiguracja aplikacji. Skontaktuj się z administratorem."

    form = ChatForm(request.POST or None)

    if request.method == 'POST' and form.is_valid() and api_key:

        try:
            user_prompt = form.cleaned_data["prompt"]
            history_json = form.cleaned_data.get("conversation_history") or "[]"
            messages = json.loads(history_json)
            if messages == []:
                messages.append({"role": "user", "content": preprompt})

            client = OpenAI(api_key=api_key)
            messages.append({"role": "user", "content": user_prompt})
            response = client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=0.7
            )
            assistant_response = response.choices[0].message.content
            messages.append({"role": "assistant", "content": assistant_response})

            form = ChatForm(initial={"conversation_history": json.dumps(messages)})

        except Exception as e:
            error_message = f"Wystąpił błąd: {str(e)}"


    return render(request, "myapp/chat.html",
                  {"form": form, "error_message": error_message,
                   "assistant_response": assistant_response, "response": response, "messages": messages})
