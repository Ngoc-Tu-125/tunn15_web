from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser, BlogPost, TechBlogPost, SocialLink
from .models import SocialLink

# Social Link
admin.site.register(SocialLink)


# Blog Post
@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'date_published',)  # Customize the fields you want to display in the list view
    search_fields = ('title',)  # Allow searching by title
    prepopulated_fields = {'slug': ('title',)}


# Tech Blog Post
@admin.register(TechBlogPost)
class TechBlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'tech_type', 'date_published',)  # Display tech_type in the list view
    search_fields = ('title', 'tech_type',)  # Allow searching by title and tech_type
    prepopulated_fields = {'slug': ('title',)}


# Custom Admin
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ('email', 'is_staff', 'is_active',)
    list_filter = ('email', 'is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)


admin.site.register(CustomUser, CustomUserAdmin)
