"""
URL configuration for course_listing project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from courses.views import course_list, course_detail, enroll_course
from courses.views import register, user_login, user_logout
from courses.views import create_course, edit_course, delete_course

app_name = 'courses'

urlpatterns = [
    # path("admin/", admin.site.urls), #default
    path('', course_list, name='course_list'),
    path('courses_list/', course_list, name='course_list'),
    path('course/<int:course_id>/', course_detail, name='course_detail'),
    path('course/<int:course_id>/enroll/', enroll_course, name='enroll_course'),
    path('register/', register, name='register'),
    path('course/register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('course/login/', user_login, name='login'),
    path('course/logout/', user_logout, name='logout'),
    path('create/', create_course, name='create_course'),
    path('edit/<int:course_id>/', edit_course, name='edit_course'),
    path('delete/<int:course_id>/', delete_course, name='delete_course'),
# will fix the paths on the go
]
