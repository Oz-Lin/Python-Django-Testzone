# Create your models here.
from django.db import models
from django.contrib.auth.models import User

class Course(models.Model):
    name = models.CharField(max_length=255)
    date = models.DateField()
    location = models.CharField(max_length=255)
    description = models.TextField()
    photo = models.ImageField(upload_to='course_photos')
    cost = models.DecimalField(max_digits=8, decimal_places=2)
    places_available = models.IntegerField()
    learning_outcomes = models.TextField()

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name