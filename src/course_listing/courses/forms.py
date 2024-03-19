from django import forms
from .models import Course, Review, Enrollment

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['title', 'instructor', 'duration', 'description', 'date', 'location', 'cost', 'places_available', 'learning_outcomes']

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['comment', 'rating']

class EnrollmentForm(forms.ModelForm):
    class Meta:
        model = Enrollment
        fields = ['student_name', 'email']