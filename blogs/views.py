from django.shortcuts import render, redirect
from django.contrib.auth import views as auth_views
from django.views.generic import CreateView, ListView
from django.contrib.auth.decorators import login_required

from .models import BlogPost
from django.contrib.auth.models import User
from .forms import BlogPostForm

def signup_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        User.objects.create_user(username=username, password=password)
        return render(request, 'registration/signup.html', {'success': 'Account created successfully! Please login.'})
    return render(request, 'registration/signup.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth_views.authenticate(request, username=username, password=password)
        if user is not None:
            auth_views.login(request, user)
            return render(request, 'home.html')
        else:
            return render(request, 'registration/login.html', {'error': 'Invalid credentials'})
    return render(request, 'registration/login.html')


def home_view(request):
    posts = BlogPost.objects.all()
    return render(request, 'home.html', {'posts': posts})
    

class BlogPostCreateView(CreateView):
    model = BlogPost
    form_class = BlogPostForm
    

@login_required
def blog_create_view(request):
    """
    Function-based view to create a new blog post.
    Handles form rendering, validation, and saving with proper author/status.
    """
    if request.method == 'POST':
        form = BlogPostForm(request.POST)
        if form.is_valid():
            blog_post = form.save(commit=False)
            blog_post.author = request.user

            # Determine status based on which button was clicked
            if 'publish' in request.POST:
                blog_post.status = 'published'
            else:
                # Default to draft when "save_draft" or generic submit happens
                blog_post.status = 'draft'

            blog_post.save()
            return redirect('blogs:home')
    else:
        form = BlogPostForm()

    return render(request, 'blogs/blog_form.html', { 'form': form })
