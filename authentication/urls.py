from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("signup", views.signup, name="signup"),
    path("signin", views.signin, name="signin"),
    path("home_screen", views.home_screen, name="home_screen"),
    path("signout", views.signout, name="signout"),
    path("activate/<uidb64>/<token>", views.activate, name="activate"),
    path("routine", views.routine, name="routine"),
    path("new_workout", views.new_workout, name="new_workout"),
]
