from django.urls import path
from .views import (
    blog_create_view,
    BlogPostListView,
    BlogPostDetailView,
    like_post,
    add_comment
)

app_name = 'blogs'


urlpatterns = [
    path('', BlogPostListView.as_view(), name='list'),
    path('create/', blog_create_view, name='create'),
    path('<int:pk>/', BlogPostDetailView.as_view(), name='detail'),
    path('<int:pk>/like/', like_post, name='like'),
    path('<int:pk>/comment/', add_comment, name='comment'),
]
