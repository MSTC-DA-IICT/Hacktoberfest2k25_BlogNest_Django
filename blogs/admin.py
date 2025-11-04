from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import BlogPost, Like, Comment


# Configure User admin for better autocomplete in BlogPost admin
# Unregister the default User admin and re-register with enhanced search
admin.site.unregister(User)

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    search_fields = ['username', 'email', 'first_name', 'last_name']


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    """
    Admin configuration for BlogPost model.
    Provides comprehensive blog management interface for superusers.
    """
    # Fields to display in the list view
    list_display = ('title', 'author', 'status', 'likes', 'created_at', 'updated_at')
    
    # Enable filtering in the sidebar
    list_filter = ('status', 'created_at', 'updated_at', 'author')
    
    # Enable search functionality
    search_fields = ('title', 'content', 'excerpt', 'tags', 'author__username')
    
    # Date hierarchy for easy navigation
    date_hierarchy = 'created_at'
    
    # Organize fields into sections
    fieldsets = (
        ('Blog Information', {
            'fields': ('title', 'excerpt', 'content', 'tags')
        }),
        ('Author & Status', {
            'fields': ('author', 'status')
        }),
        ('Engagement', {
            'fields': ('likes',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    # Make timestamps read-only
    readonly_fields = ('created_at', 'updated_at')
    
    # Order by most recent first
    ordering = ('-created_at',)
    
    # Number of items per page
    list_per_page = 25
    
    # Enable quick edit for status
    list_editable = ('status',)
    
    # Auto-complete for author field
    autocomplete_fields = ['author']


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    """
    Admin configuration for Like model.
    """
    list_display = ('user', 'blog_post', 'created_at')
    list_filter = ('created_at', 'blog_post')
    search_fields = ('user__username', 'blog_post__title')
    readonly_fields = ('created_at',)
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """
    Admin configuration for Comment model.
    """
    list_display = ('user', 'blog_post', 'content_preview', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at', 'blog_post')
    search_fields = ('user__username', 'blog_post__title', 'content')
    readonly_fields = ('created_at', 'updated_at')
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)
    
    fieldsets = (
        ('Comment Information', {
            'fields': ('blog_post', 'user', 'content')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def content_preview(self, obj):
        """Show first 50 characters of comment"""
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
    content_preview.short_description = 'Content Preview'
