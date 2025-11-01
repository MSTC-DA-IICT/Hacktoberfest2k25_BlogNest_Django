from django.urls import path
from .views import blog_create_view

app_name = 'blogs'


urlpatterns = [
    path('create/', blog_create_view, name='create'),
]
