from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from .models import Course, Enrollment
from .forms import CourseForm

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

@login_required
def create_course(request):
    if request.method == 'POST':
        form = CourseForm(request.POST, request.FILES)
        if form.is_valid():
            course = form.save(commit=False)
            course.user = request.user
            course.save()
            return redirect('home')
    else:
        form = CourseForm()
    return render(request, 'courses/create_course.html', {'form': form})


@login_required
def edit_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    if request.user == course.user:
        if request.method == 'POST':
            form = CourseForm(request.POST, request.FILES, instance=course)
            if form.is_valid():
                form.save()
                return redirect('home')
        else:
            form = CourseForm(instance=course)
        return render(request, 'courses/edit_course.html', {'form': form})
    else:
        return redirect('home')


@login_required
def delete_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    if request.user == course.user:
        course.delete()
    return redirect('home')

@login_required
def my_courses(request):
    courses = Course.objects.filter(user=request.user)
    return render(request, 'my_courses.html', {'courses': courses})