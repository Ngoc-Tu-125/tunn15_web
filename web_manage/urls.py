"""
URL configuration for web_manage project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from web_app import views
from django.contrib.sitemaps.views import sitemap
from web_app.sitemaps import StaticViewSitemap, BlogSitemap, TechBlogSitemap, EbookPicturesSitemap


sitemaps = {
    'static': StaticViewSitemap,
    'blog': BlogSitemap,
    'techblog': TechBlogSitemap,
    'ebook_pictures': EbookPicturesSitemap,
}



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),

    path('custom-admin/', views.custom_admin, name='custom_admin'),

    path('home/', views.home, name='home'),
    path('upload-image/<str:section_name>/', views.upload_image, name='upload_image'),
    path('save-content/<str:section_name>/', views.save_content, name='save_content'),

    path('blog/', views.blog_home, name='blog'),
    path('blog/<slug:post_slug>/', views.blog_detail, name='blog_detail'),
    path('ckeditor/', include('ckeditor_uploader.urls')),

    path('tech_blog/', views.tech_blog_home, name='tech_blog'),
    path('tech_blog/<slug:post_slug>/', views.tech_blog_detail, name='tech_blog_detail'),

    path('ebook_pictures/', views.ebook_pictures, name='ebook_pictures'),
    path('ebook_pictures/<int:card_id>/', views.ebook_picture_details, name='ebook_picture_details'),

    path('contacts/', views.contacts, name='contacts'),

    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('check_email/', views.check_email_exists, name='check_email_exists'),

    path('filter_tech_blog_posts/', views.filter_tech_blog_posts, name='filter_tech_blog_posts'),

    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
