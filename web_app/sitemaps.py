# sitemaps.py

from django.contrib import sitemaps
from django.urls import reverse
from .models import BlogPost, TechBlogPost, Card

class StaticViewSitemap(sitemaps.Sitemap):
    priority = 0.7
    changefreq = 'daily'

    def items(self):
        return ['home', 'contacts', 'signup', 'login']

    def location(self, item):
        return reverse(item)

class BlogSitemap(sitemaps.Sitemap):
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        return BlogPost.objects.all()

    def lastmod(self, obj):
        return obj.date_published

class TechBlogSitemap(sitemaps.Sitemap):
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        return TechBlogPost.objects.exclude(tech_type='raft')

    def lastmod(self, obj):
        return obj.date_published

class EbookPicturesSitemap(sitemaps.Sitemap):
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        return Card.objects.all()

