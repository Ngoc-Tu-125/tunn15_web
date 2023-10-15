import json
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login as auth_login, authenticate
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .forms import CustomUserCreationForm
from .models import CustomUser, BlogPost, TechBlogPost
from .models import HomePageContent
from .models import SocialLink, PLATFORM_CHOICES
from .models import Card


from django.conf import settings

def filter_tech_blog_posts(request):
    tech_type = request.GET.get('techType')

    # Query the TechBlogPost model to get the filtered posts
    posts = TechBlogPost.objects.filter(tech_type=tech_type)

    # Convert the QuerySet to a list of dictionaries with full image URLs
    posts_list = [{
        'title': post.title,
        'image_url': settings.MEDIA_URL + str(post.image) if post.image else None,
        'slug': post.slug,
        'date_published': post.date_published,
        'body_snippet': post.body_snippet
    } for post in posts]

    return JsonResponse(posts_list, safe=False)

####################################################################################
# Utility Functions
####################################################################################
def get_social_links():
    platform_order = {name[0]: index for index, name in enumerate(PLATFORM_CHOICES)}
    return sorted(SocialLink.objects.all(), key=lambda x: platform_order[x.platform])

####################################################################################
# Error Handling
####################################################################################
def error_500_view(request, exception=None):
    return render(request, 'error_500.html'), 500


####################################################################################
# MAIN VIEWS
####################################################################################
def contacts(request):
    # Context data
    context = {
        'social_links': get_social_links(),
    }
    return render(request, 'contacts/contacts.html', context)


####################################################################################
# EDIT HOME PAGE
####################################################################################
def home(request):
    is_staff = request.user.is_staff
    intro_content = HomePageContent.objects.get_or_create(section_name='intro', defaults={'title': "Xin chào", 'content': "Rất vui vì mọi người đã ghé thăm trang web nhỏ này."})[0]
    delivery_content = HomePageContent.objects.get_or_create(section_name='delivery', defaults={'title': "Về Bản Thân Mình", 'content': "Vài thông tin nhỏ"})[0]
    success_story_content = HomePageContent.objects.get_or_create(section_name='success', defaults={'title': "Vài chia sẻ nhỏ của mình", 'content': "Vài câu chuyện nhỏ"})[0]

    # Full context:
    # Context data
    context = {
            'intro_content': intro_content,
            'delivery_content': delivery_content,
            'success_story_content': success_story_content,
            'is_staff': is_staff,
            'social_links': get_social_links(),
        }

    return render(request, 'home/home.html', context)

@csrf_exempt
def upload_image(request, section_name):
    if request.method == 'POST' and request.user.is_staff:
        uploaded_image = request.FILES.get('image')

        # Get the specific section or create a new one if none exists
        section_content, _ = HomePageContent.objects.get_or_create(section_name=section_name)

        # Update the image
        section_content.image = uploaded_image
        section_content.save()

        return JsonResponse({'success': True})

    return JsonResponse({'success': False})

@csrf_exempt
def save_content(request, section_name):
    if request.method == 'POST' and request.user.is_staff:
        data = json.loads(request.body)
        title = data.get('title')
        content = data.get('content')

        # Get the specific section or create a new one if none exists
        section_content, _ = HomePageContent.objects.get_or_create(section_name=section_name)

        # Update the title and content
        if title:
            section_content.title = title
        if content:
            section_content.content = content
        section_content.save()

        return JsonResponse({'success': True})

    return JsonResponse({'success': False})

####################################################################################
# Authentication Views VIEWS
####################################################################################
def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)  # Log the user in after signing up
            # Redirect to a success page or home page after signup
            return redirect('home')
        else:
            print(form.errors)
            if 'email' in form.errors:
                messages.error(request, 'An account with this email already exists. Please use a different email or log in.')
            else:
                messages.error(request, 'There was an error with your signup. Please check the details and try again.')
    else:
        form = CustomUserCreationForm()

    return render(request, 'auth/login.html', {'form': form})


def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        print("DEBUG:", email, password)
        user = authenticate(request, email=email, password=password)
        if user is not None:
            auth_login(request, user)
            # Redirect to home page after successful login
            return redirect('home')
        else:
            messages.error(request, 'Invalid email or password.')
    return render(request, 'auth/login.html')


def logout(request):
    auth_logout(request)
    return redirect('home')


def check_email_exists(request):
    email = request.GET.get('email', None)
    exists = CustomUser.objects.filter(email=email).exists()

    return JsonResponse({'exists': exists})


####################################################################################
# BLOG PAGE
####################################################################################
def blog_home(request):
    # Get edit info
    is_staff = request.user.is_staff
    about_content = HomePageContent.objects.get_or_create(
        section_name='about',
        defaults={'title': "VỀ MÌNH", 'content': "I find life better, and I'm happier, when things are nice and simple."}
    )[0]

    articles_list = BlogPost.objects.all().order_by('-date_published')
    paginator = Paginator(articles_list, 3)  # Show 10 articles per page

    page = request.GET.get('page')
    try:
        articles = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        articles = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        articles = paginator.page(paginator.num_pages)

    if articles:
        # Add a class attribute for the template to the latest article
        articles[0].class_name = "article-featured"

        # For the rest of the articles, assign the class 'article-recent'
        for article in articles[1:]:
            article.class_name = "article-recent"

    # Fetch the three latest posts for the sidebar
    lastest_posts = BlogPost.objects.all().order_by('-date_published')[:3]


    # Context data
    context = {
        'articles': articles,
        'lastest_posts': lastest_posts,
        'social_links': get_social_links(),
        'about_content': about_content,
        'is_staff': is_staff,
    }
    # Render the blog page with the fetched articles and lastest_posts
    return render(request, 'blog/main_blog.html', context)


def blog_detail(request, post_slug):
    # Fetch the blog post based on the provided slug
    post = get_object_or_404(BlogPost, slug=post_slug)

    # Fetch the three latest posts for the sidebar
    lastest_posts = BlogPost.objects.all().order_by('-date_published')[:3]


    # Context data
    context = {
        'post': post,
        'lastest_posts': lastest_posts,
        'social_links': get_social_links(),
    }

    # Render the detailed view template
    return render(request, 'blog/blog_detail_template.html', context)


####################################################################################
# TECH BLOG PAGE
####################################################################################
def tech_blog_home(request):
    # Get edit info
    is_staff = request.user.is_staff
    about_content = HomePageContent.objects.get_or_create(
        section_name='about',
        defaults={'title': "VỀ MÌNH", 'content': "I find life better, and I'm happier, when things are nice and simple."}
    )[0]

    # Get technical articles list
    tech_articles_list = TechBlogPost.objects.all().order_by('-date_published')
    paginator = Paginator(tech_articles_list, 3)  # Show 3 tech articles per page

    page = request.GET.get('page')
    try:
        tech_articles = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver the first page.
        tech_articles = paginator.page(1)
    except EmptyPage:
        # If page is out of range, deliver the last page of results.
        tech_articles = paginator.page(paginator.num_pages)

    if tech_articles:
        # Add a class attribute for the template to the latest tech article
        tech_articles[0].class_name = "article-featured"
        # For the rest of the tech articles, assign the class 'article-recent'
        for article in tech_articles[1:]:
            article.class_name = "article-recent"

    # Fetch the three latest tech posts for the sidebar
    latest_tech_posts = TechBlogPost.objects.all().order_by('-date_published')[:3]

    # Get tech blog type
    tech_blog_types = [
        {"type": "python", "display_name": "Python", "icon": "fab fa-python"},
        {"type": "cpp", "display_name": "C/C++", "icon": "fab fa-cuttlefish"},
        {"type": "test", "display_name": "Test", "icon": "fas fa-file-code"},
        {"type": "other", "display_name": "Other", "icon": "fas fa-laptop-code"},
    ]

    # Context data
    context = {
        'tech_articles': tech_articles,
        'latest_tech_posts': latest_tech_posts,
        'social_links': get_social_links(),
        'about_content': about_content,
        'tech_blog_types': tech_blog_types,
        'is_staff': is_staff,
    }
    # Render the tech blog page with the fetched tech articles and latest_tech_posts
    return render(request, 'tech_blog/main_tech_blog.html', context)


def tech_blog_detail(request, post_slug):
    # Fetch the tech blog post based on the provided slug
    tech_post = get_object_or_404(TechBlogPost, slug=post_slug)

    # Fetch the three latest tech posts for the sidebar
    latest_tech_posts = TechBlogPost.objects.all().order_by('-date_published')[:3]

    # Context data
    context = {
        'tech_post': tech_post,
        'latest_tech_posts': latest_tech_posts,
        'social_links': get_social_links(),
    }

    # Render the detailed tech blog view template
    return render(request, 'tech_blog/tech_blog_detail_template.html', context)


####################################################################################
# EBOOK PICTURES PAGE
####################################################################################
def ebook_pictures(request):
    cards = Card.objects.all()

    # Get contex for web
    context = {
        'cards': cards,
        'social_links': get_social_links(),
    }

    if request.user.is_authenticated:
        return render(request, 'ebook_pictures/ebook_pictures.html', context)
    else:
        return render(request, 'auth/login_required_prompt.html', context)


def ebook_picture_details(request, card_id):
    card = Card.objects.get(id=card_id)
    images = card.imagedetail_set.all()

    # Get contex for web
    context = {
        'card': card,
        'images': images,
        'social_links': get_social_links(),
    }

    return render(request, 'ebook_pictures/ebook_picture_details.html', context)


####################################################################################
# CUSTOM ADMIN PAGE
####################################################################################
@user_passes_test(lambda u: u.is_superuser)
def custom_admin(request):
    return render(request, 'custom_admin/custom_admin.html')