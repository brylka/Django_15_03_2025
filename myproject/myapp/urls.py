from django.urls import path
from .views import hello_world, hello_name, add, divide, table, post_list

urlpatterns = [
    path('hello/', hello_world),
    path('hello/<str:name>/', hello_name),
    path('add/<int:a>/<int:b>/', add),
    path('divide/<int:a>/<int:b>/', divide),
    path('table/', table),

    path('posts/', post_list)
]