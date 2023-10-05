from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login, authenticate
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .forms import CustomUserCreationForm
from .models import CustomUser


####################################################################################
# MAIN VIEWS
####################################################################################
def home(request):
    return render(request, 'home.html')


def blog(request):
    return render(request, 'main_blog.html')


def tech_blog(request):
    return render(request, 'main_tech_blog.html')

def ebook_pictures(request):
    if request.user.is_authenticated:
        return render(request, 'ebook_pictures.html')
    else:
        return render(request, 'login_required_prompt.html')


def contacts(request):
    return render(request, 'contacts.html')


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
            if 'email' in form.errors:
                messages.error(request, 'An account with this email already exists. Please use a different email or log in.')
            else:
                messages.error(request, 'There was an error with your signup. Please check the details and try again.')
    else:
        form = CustomUserCreationForm()

    return render(request, 'login.html', {'form': form})

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
    return render(request, 'login.html')

def logout(request):
    auth_logout(request)
    return redirect('home')
