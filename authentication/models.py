from django.db import models

# Create your models here.
# models.py in your app


class Exercise(models.Model):
    workout_name = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    set_number = models.IntegerField()
    weight = models.FloatField()
    reps = models.IntegerField()



from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    field1 = models.CharField(max_length=255)
    field2 = models.CharField(max_length=255)

    def __str__(self):
        return self.user.username