from django.urls import path
from .views import hello_world, hello_name, add, divide, table, post_list, create_post, update_post, delete_post, \
    zero_point, chat

urlpatterns = [
    path('hello/', hello_world),
    path('hello/<str:name>/', hello_name),
    path('add/<int:a>/<int:b>/', add),
    path('divide/<int:a>/<int:b>/', divide),
    path('table/', table, name='table'),

    path('posts/', post_list, name='post_list'),
    path('posts/create/', create_post, name='create_post'),
    path('posts/update/<int:post_id>', update_post, name='update_post'),
    path('posts/delete/<int:post_id>', delete_post, name='delete_post'),

    path('zero-point/', zero_point, name='zero_point'),

    path('chat/', chat, name='chat'),
]