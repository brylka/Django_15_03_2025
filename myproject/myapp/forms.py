from django import forms

from .models import Post


class LinearEquationForm(forms.Form):
    a = forms.FloatField(label="Współczynnik a")
    b = forms.FloatField(label="Współczynnik b")


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["title", "content"]
        labels = {"title": "Tytuł posta", "content": "Treść posta"}
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control", "placeholder": "Podaj tytuł"}),
            "content": forms.Textarea(attrs={"class": "form-control", "placeholder": "Podaj treść posta", "rows": 5}),
        }
