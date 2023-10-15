from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from adminsortable2.admin import SortableAdminMixin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser, BlogPost, TechBlogPost, SocialLink
from .models import SocialLink, HomePageContent
from .models import Card, ImageDetail

# Social Link
admin.site.register(SocialLink)

# Home page content
@admin.register(HomePageContent)
class HomePageContentAdmin(admin.ModelAdmin):
    list_display = ['section_name', 'title']

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


# Ebook pictures
@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    list_display = ['title', 'short_intro', 'order']
    list_editable = ['order']  # Allow editing order directly from the admin list view

@admin.register(ImageDetail)
class ImageDetailAdmin(admin.ModelAdmin):
    list_display = ['card', 'caption', 'order']
    list_editable = ['order']  # Allow editing order directly from the admin list view


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
