from django.utils.encoding import force_str as force_text
from django.utils.encoding import force_bytes
from django.core.mail import EmailMessage
from base64 import urlsafe_b64decode, urlsafe_b64encode
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.mail import send_mail
from gfg import settings
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from .tokens import generate_token
from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User


# Create your views here.

def home(request):
    return render(request, "index.html")


def signup(request):
    if request.method == "POST":
        username = request.POST["username"]
        fname = request.POST["fname"]
        lname = request.POST["lname"]
        email = request.POST["email"]
        pass1 = request.POST["pass1"]
        pass2 = request.POST["pass2"]

        if User.objects.filter(username=username):
            messages.error(request, "Username already exists")
            return redirect("signup")

        if len(username) <= 7:
            messages.error(request, "Username should be greater than 5 chars")
            return redirect("signup")
        if not len(pass1) > 5:
            messages.error(request, "min length of password is 8 chars")
            return redirect("signup")

        if pass1 != pass2:
            messages.error(request, "Passwords did not match")
            return redirect("signup")

        if not username.isalnum():
            messages.error(request, "Username must be alpha-numeric")
            return redirect("signup")

        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.is_active = False
        myuser.save()

        messages.success(
            request, "Your account has been created successfully. Login to continue"
        )

        # Welcome email
        subject = "Welcome"
        message = f"Hello {myuser.first_name}!! Thank you for visiting our website. Check another mail for confirmation."
        from_email = settings.EMAIL_HOST_USER
        to_list = [myuser.email]
        send_mail(subject, message, from_email, to_list)

        # conformation email
        current_site = get_current_site(request)
        email_subject = "confirm your email..!!"
        message2 = render_to_string(
            "email_conformation.html",
            {
                "name": myuser.first_name,
                "domain": current_site.domain,
                "uid": urlsafe_b64encode(force_bytes(myuser.pk)),
                "token": generate_token.make_token(myuser),
            },
        )

        email = EmailMessage(
            email_subject,
            message2,
            settings.EMAIL_HOST_USER,
            [myuser.email],
        )
        email.fail_silently = False
        email.send()
        
        
        return redirect("home")

    return render(request, "signup.html")


def signin(request):
    if request.method == "POST":
        username = request.POST["username"]
        pass1 = request.POST["pass1"]
        user = authenticate(request, username=username, password=pass1)
        if user is not None:
            login(request, user)
            fname = user.first_name
            messages.success(request, "logged in successfully")
            messages.error(request, "Wrong Credentials,signin again")
            return render(request, "home_screen.html", {"username": username})
        else:
            messages.error(request, "Wrong credentials")
            return redirect("home_screen")

    return render(request, "signin.html")


def signout(request):
    logout(request)
    messages.success(request, "logged out successfully")
    return redirect("home")


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_b64decode(uidb64))
        myuser = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        myuser = None

    if myuser is not None and generate_token.check_token(myuser, token):
        myuser.is_active = True
        myuser.profile.signup_confirmation = True
        myuser.save()
        login(request, myuser)  
        messages.success(request, "Your Account has been activated!!")
        return redirect("signin")
    else:
        return render(request, "activation_failed.html")
def routine(request):
    return render(request,"routine.html")
def home_screen(request):
    return render(request,"home_screen.html")
def new_workout(request):
    return render(request,"new_workout.html")
from .models import Exercise

# views.py

from .models import UserProfile

def create_post(request):
    if request.method == 'POST':
        # Access the posted data
        field1 = request.POST.get('field1')
        field2 = request.POST.get('field2')

        # Get the currently logged-in user
        user = request.user

        # Create a new instance of your UserProfile model
        user_profile = UserProfile(user=user, field1=field1, field2=field2)

        # Save the instance to the database
        user_profile.save()

        # Redirect to a success page or render a template
        return redirect('success_page')

    return render(request, 'example_form.html')
