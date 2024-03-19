from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from .models import Course, Review, Enrollment
from .forms import CourseForm, ReviewForm, EnrollmentForm

# Create your views here.
def course_list(request):
    courses = Course.objects.all()
    return render(request, 'courses/course_list.html', {'courses': courses})

def course_detail(request, course_id):
    course = Course.objects.get(id=course_id)
    reviews = Review.objects.filter(course=course)
    enrollment_form = EnrollmentForm()
    return render(request, 'courses/course_detail.html', {'course': course, 'reviews': reviews, 'enrollment_form': enrollment_form})

def enroll_course(request, course_id):
    course = Course.objects.get(id=course_id)
    if request.method == 'POST':
        enrollment_form = EnrollmentForm(request.POST)
        if enrollment_form.is_valid():
            enrollment = enrollment_form.save(commit=False)
            enrollment.course = course
            enrollment.save()
            return redirect('course_detail', course_id=course_id)
    else:
        enrollment_form = EnrollmentForm()
    return render(request, 'courses/course_detail.html', {'course': course, 'enrollment_form': enrollment_form})

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


def homepage(request):
    courses = Course.objects.all().order_by('-date')[:10]
    return render(request, 'courses/homepage.html', {'courses': courses})

def search(request):
    # Handle search functionality here
    return render(request, 'courses/search.html')

def filter(request):
    # Handle filter functionality here
    return render(request, 'courses/filter.html')

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
    return render(request, 'courses/my_courses.html', {'courses': courses})