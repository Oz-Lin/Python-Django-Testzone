from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from .models import Course, Review, Enrollment, Comment
from django.contrib import messages
from .forms import CourseForm, ReviewForm, EnrollmentForm, CommentForm, RatingForm
from django.db.models import Q # search func
from django.core.paginator import Paginator # pagination to the course list page

# Create your views here.
def course_list(request):
    query = request.GET.get('q')

    if query:
        courses = Course.objects.filter(
            Q(title__icontains=query) |
            Q(instructor__icontains=query) |
            Q(description__icontains=query)
        )
    else:
        courses = Course.objects.all()

    paginator = Paginator(courses, 10)  # Display 10 courses per page

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'courses/course_list.html', {'page_obj': page_obj, 'query': query})

def course_detail(request, course_id):
    course = Course.objects.get(id=course_id)
    enrollments = Enrollment.objects.filter(course=course)
    enrollment_form = EnrollmentForm()
    comment_form = CommentForm()
    rating_form = RatingForm()

    if request.method == 'POST':
        if 'enrollment_form' in request.POST:
            enrollment_form = EnrollmentForm(request.POST)
            if enrollment_form.is_valid():
                name = enrollment_form.cleaned_data['name']
                email = enrollment_form.cleaned_data['email']

                # Check if the user is already enrolled
                if Enrollment.objects.filter(course=course, email=email).exists():
                    messages.warning(request, 'You are already enrolled in this course!')
                else:
                    enrollment = enrollment_form.save(commit=False)
                    enrollment.course = course
                    enrollment.save()
                    messages.success(request, f'Congratulations, {name}! You have successfully enrolled in the course!')
                    return redirect('course_detail', course_id=course_id)
            else:
                for field, errors in enrollment_form.errors.items():
                    for error in errors:
                        messages.error(request, f'{field.capitalize()}: {error}')
        else:
            initial_data = {'name': request.user.get_full_name(),
                        'email': request.user.email} if request.user.is_authenticated else None
            enrollment_form = EnrollmentForm(initial=initial_data)

    elif 'comment_form' in request.POST:
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.course = course
            comment.user = request.user
            comment.save()
            messages.success(request, 'Your comment has been posted.')
            return redirect('course_detail', course_id=course_id)

    elif 'rating_form' in request.POST:
        rating_form = RatingForm(request.POST)
        if rating_form.is_valid():
            rating = rating_form.save(commit=False)
            rating.course = course
            rating.user = request.user
            rating.save()
            messages.success(request, 'Thank you for rating the course.')
            return redirect('course_detail', course_id=course_id)

    return render(request, 'courses/course_detail.html', {'course': course, 'enrollments': enrollments,
                                                          'enrollment_form': enrollment_form,
                                                          'comment_form': comment_form,
                                                          'rating_form': rating_form})

def enroll_course(request, course_id):
    course = Course.objects.get(id=course_id)
    if request.method == 'POST':
        enrollment_form = EnrollmentForm(request.POST)
        if enrollment_form.is_valid():
            name = enrollment_form.cleaned_data['name']
            email = enrollment_form.cleaned_data['email']

            # Check if the user is already enrolled
            if Enrollment.objects.filter(course=course, email=email).exists():
                messages.warning(request, 'You are already enrolled in this course!')
            else:
                enrollment = enrollment_form.save(commit=False)
                enrollment.course = course
                enrollment.save()

                # Update the number of available places for the course
                course.places_available -= 1
                course.save()

                messages.success(request, f'Congratulations, {name}! You have successfully enrolled in the course!')
                return redirect('course_detail', course_id=course_id)
        else:
            for field, errors in enrollment_form.errors.items():
                for error in errors:
                    messages.error(request, f'{field.capitalize()}: {error}')
    else:
        initial_data = {'name': request.user.get_full_name(),
                        'email': request.user.email} if request.user.is_authenticated else None
        enrollment_form = EnrollmentForm(initial=initial_data)
    return render(request, 'courses/course_detail.html', {'course': course, 'enrollment_form': enrollment_form})

def cancel_enrollment(request, enrollment_id):
    enrollment = Enrollment.objects.get(id=enrollment_id)

    # Check if the current user is the owner of the enrollment
    if request.user == enrollment.user:
        course = enrollment.course
        enrollment.delete()

        # Update the number of available places for the course
        course.places_available += 1
        course.save()

        messages.success(request, 'You have successfully canceled your enrollment.')
    else:
        messages.error(request, 'You are not authorized to cancel this enrollment.')

    return redirect('course_detail', course_id=course.id)

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