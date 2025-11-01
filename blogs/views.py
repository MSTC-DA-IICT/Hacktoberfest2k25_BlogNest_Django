from django.shortcuts import render, redirect
from django.contrib.auth import views as auth_views
from django.views.generic import CreateView, ListView
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm

from .models import BlogPost
from django.contrib.auth.models import User
from .forms import BlogPostForm, UserSignupForm

def signup_view(request):
    if request.method == 'POST':
        form = UserSignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Automatically log in the user after signup
            return redirect('home')  # Redirect to home page after successful signup
    else:
        form = UserSignupForm()
    return render(request, 'registration/signup.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'registration/login.html', {'form': form, 'error': 'Invalid username or password'})
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})


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
            return redirect('home')
    else:
        form = BlogPostForm()

    return render(request, 'blogs/blog_form.html', { 'form': form })
