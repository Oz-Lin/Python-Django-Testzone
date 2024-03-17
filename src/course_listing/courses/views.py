from django.shortcuts import render, redirect
from .models import Course, Enrollment
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout

# Create your views here.
def course_list(request):
    courses = Course.objects.all()
    return render(request, 'courses/course_list.html', {'courses': courses})

def course_detail(request, course_id):
    course = Course.objects.get(id=course_id)
    return render(request, 'courses/course_detail.html', {'course': course})

def enroll_course(request, course_id):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        course = Course.objects.get(id=course_id)
        enrollment = Enrollment(name=name, email=email, course=course)
        enrollment.save()
        return render(request, 'courses/enroll_success.html')
    else:
        return redirect('course_detail', course_id=course_id)


# User account module
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'courses/register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'courses/login.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('home')