import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login as auth_login, authenticate
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .forms import CustomUserCreationForm
from .models import CustomUser, BlogPost
from .models import HomePageContent
from .models import SocialLink, PLATFORM_CHOICES


####################################################################################
# MAIN VIEWS
####################################################################################
def tech_blog(request):
    return render(request, 'tech_blog/main_tech_blog.html')

def ebook_pictures(request):
    if request.user.is_authenticated:
        return render(request, 'ebook_pictures/ebook_pictures.html')
    else:
        return render(request, 'auth/login_required_prompt.html')

def contacts(request):
    platform_order = {name[0]: index for index, name in enumerate(PLATFORM_CHOICES)}
    social_links = sorted(SocialLink.objects.all(), key=lambda x: platform_order[x.platform])
    return render(request, 'contacts/contacts.html', {'social_links': social_links})


####################################################################################
# EDIT HOME PAGE
####################################################################################
def home(request):
    is_staff = request.user.is_staff
    intro_content = HomePageContent.objects.get_or_create(section_name='intro', defaults={'title': "Xin chào", 'content': "Rất vui vì mọi người đã ghé thăm trang web nhỏ này."})[0]
    delivery_content = HomePageContent.objects.get_or_create(section_name='delivery', defaults={'title': "Về Bản Thân Mình", 'content': "Vài thông tin nhỏ"})[0]
    success_story_content = HomePageContent.objects.get_or_create(section_name='success', defaults={'title': "Vài chia sẻ nhỏ của mình", 'content': "Vài câu chuyện nhỏ"})[0]

    # Process with footer
    platform_order = {name[0]: index for index, name in enumerate(PLATFORM_CHOICES)}
    social_links = sorted(SocialLink.objects.all(), key=lambda x: platform_order[x.platform])

    # Full context:
    context = {
            'intro_content': intro_content,
            'delivery_content': delivery_content,
            'success_story_content': success_story_content,
            'is_staff': is_staff,
            'social_links': social_links,
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
# SIGN IN VIEWS
####################################################################################

def check_email_exists(request):
    email = request.GET.get('email', None)
    exists = CustomUser.objects.filter(email=email).exists()

    return JsonResponse({'exists': exists})


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


####################################################################################
# BLOG PAGE
####################################################################################
def blog_home(request):
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

    # Render the blog page with the fetched articles and lastest_posts
    return render(request, 'blog/main_blog.html', {'articles': articles, 'lastest_posts': lastest_posts})


def blog_detail(request, post_slug):
    # Fetch the blog post based on the provided slug
    post = get_object_or_404(BlogPost, slug=post_slug)

    # Fetch the three latest posts for the sidebar
    lastest_posts = BlogPost.objects.all().order_by('-date_published')[:3]

    # Render the detailed view template
    return render(request, 'blog/blog_detail_template.html', {'post': post, 'lastest_posts': lastest_posts})