from django.shortcuts import render
from django.contrib.auth import views as auth_views


from .models import User, BlogPost

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
    

