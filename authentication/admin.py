from django.contrib import admin

# Register your models here.
# admin.py in your app

from .models import Exercise,UserProfile

admin.site.register(Exercise)
admin.site.register(UserProfile)