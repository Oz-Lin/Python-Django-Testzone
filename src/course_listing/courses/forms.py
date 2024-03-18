from django import forms
from .models import Course

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['user', 'name', 'date', 'location', 'description', 'photo', 'cost',
                  'places_available', 'learning_outcomes']