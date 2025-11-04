from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import views as auth_views
from django.views.generic import CreateView, ListView, DetailView
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib import messages

from .models import BlogPost, Like, Comment
from django.contrib.auth.models import User
from .forms import BlogPostForm, UserSignupForm, CommentForm

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
    posts = BlogPost.objects.filter(status='published').order_by('-created_at')
    return render(request, 'home.html', {'posts': posts})


class BlogPostListView(ListView):
    """List view for blog posts"""
    model = BlogPost
    template_name = 'blogs/blog_list.html'
    context_object_name = 'posts'
    paginate_by = 10
    
    def get_queryset(self):
        """Filter to show only published posts"""
        return BlogPost.objects.filter(status='published').order_by('-created_at')
    

class BlogPostDetailView(DetailView):
    """Detail view for a single blog post"""
    model = BlogPost
    template_name = 'blogs/blog_detail.html'
    context_object_name = 'post'
    
    def get_queryset(self):
        """Filter to show only published posts"""
        return BlogPost.objects.filter(status='published')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.get_object()
        
        # Check if user has liked this post
        context['is_liked'] = post.is_liked_by_user(self.request.user)
        context['like_count'] = post.get_like_count()
        
        # Get comments for this post
        context['comments'] = post.comments.all()
        
        # Add comment form
        context['comment_form'] = CommentForm()
        
        return context
    

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
            return redirect('blogs:detail', pk=blog_post.pk)
    else:
        form = BlogPostForm()

    return render(request, 'blogs/blog_form.html', { 'form': form })


@login_required
@require_POST
def like_post(request, pk):
    """Like or unlike a blog post"""
    post = get_object_or_404(BlogPost, pk=pk, status='published')
    user = request.user
    
    like, created = Like.objects.get_or_create(user=user, blog_post=post)
    
    if not created:
        # User already liked, so unlike
        like.delete()
        liked = False
        messages.info(request, 'You unliked this post.')
    else:
        # User liked the post
        liked = True
        messages.success(request, 'You liked this post!')
    
    # Update the likes count in the post model (for backward compatibility)
    post.likes = post.get_like_count()
    post.save()
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        # AJAX request
        return JsonResponse({
            'liked': liked,
            'like_count': post.get_like_count()
        })
    
    return redirect('blogs:detail', pk=post.pk)


@login_required
@require_POST
def add_comment(request, pk):
    """Add a comment to a blog post"""
    post = get_object_or_404(BlogPost, pk=pk, status='published')
    form = CommentForm(request.POST)
    
    if form.is_valid():
        comment = form.save(commit=False)
        comment.blog_post = post
        comment.user = request.user
        comment.save()
        messages.success(request, 'Your comment has been added!')
    else:
        messages.error(request, 'There was an error with your comment. Please try again.')
    
    return redirect('blogs:detail', pk=post.pk)
