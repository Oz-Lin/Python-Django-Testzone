# Create your models here.
from django.db import models
from django.contrib.auth.models import User

class Course(models.Model):
    title = models.CharField(max_length=100)
    instructor = models.CharField(max_length=100)
    duration = models.IntegerField()
    description = models.TextField()
    date = models.DateField()
    location = models.CharField(max_length=100)
    cost = models.DecimalField(max_digits=8, decimal_places=2)
    places_available = models.IntegerField()
    learning_outcomes = models.TextField()

    def __str__(self):
        return self.name

class Enrollment(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    student_name = models.CharField(max_length=100)
    email = models.EmailField()

    def __str__(self):
        return f"{self.student_name} - {self.course.title}"

class Review(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField()
    comment = models.TextField()


class Comment(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.user.username} on {self.course.title}'