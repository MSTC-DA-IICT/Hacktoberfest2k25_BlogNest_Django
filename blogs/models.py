from django.db import models

# for simplification, we will use default user model provided by django auth
from django.contrib.auth.models import User


class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    excerpt = models.CharField(max_length=300, blank=True, help_text="Short description of the blog post")
    author = models.ForeignKey(User, on_delete=models.CASCADE) 
    likes = models.IntegerField(default=0)
    tags = models.CharField(max_length=200, blank=True, help_text="Comma-separated tags")
    status = models.CharField(max_length=20, choices=[('draft', 'Draft'), ('published', 'Published')], default='draft')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
    def get_like_count(self):
        """Get the actual count of likes from Like model"""
        return self.likes_set.count()
    
    def is_liked_by_user(self, user):
        """Check if a user has liked this post"""
        if not user.is_authenticated:
            return False
        return self.likes_set.filter(user=user).exists()


class Like(models.Model):
    """Model to track likes on blog posts"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    blog_post = models.ForeignKey(BlogPost, on_delete=models.CASCADE, related_name='likes_set')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user', 'blog_post')  # Prevent duplicate likes
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} liked {self.blog_post.title}"


class Comment(models.Model):
    """Model to store comments on blog posts"""
    blog_post = models.ForeignKey(BlogPost, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Comment by {self.user.username} on {self.blog_post.title}"