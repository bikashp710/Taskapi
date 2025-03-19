from django.urls import path
from .views import blog_post_list_create, blog_post_detail

urlpatterns = [
    path('', blog_post_list_create, name='blog-list'),
    path('blog-list-create/', blog_post_list_create, name='blog-list-create'),
    path('<int:pk>/', blog_post_detail, name='blog-detail'),
]
