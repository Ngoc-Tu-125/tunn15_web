from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login as auth_login, authenticate
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .forms import CustomUserCreationForm
from .models import CustomUser, BlogPost


####################################################################################
# MAIN VIEWS
####################################################################################
def home(request):
    return render(request, 'home/home.html')


def tech_blog(request):
    return render(request, 'tech_blog/main_tech_blog.html')

def ebook_pictures(request):
    if request.user.is_authenticated:
        return render(request, 'ebook_pictures/ebook_pictures.html')
    else:
        return render(request, 'auth/login_required_prompt.html')

def contacts(request):
    return render(request, 'contacts/contacts.html')


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
    # Fetch all blog posts from the database
    articles = BlogPost.objects.all()

    # Add a class attribute for the template. For simplicity, we'll use the same class for all articles here.
    for article in articles:
        article.class_name = "article-featured"  # You can modify this logic to differentiate between featured and recent articles

    # Render the blog page with the fetched articles
    return render(request, 'blog/main_blog.html', {'articles': articles})


def blog_detail(request, post_slug):
    # Fetch the blog post based on the provided slug
    post = get_object_or_404(BlogPost, slug=post_slug)

    # Render the detailed view template
    return render(request, 'blog/blog_detail_template.html', {'post': post})