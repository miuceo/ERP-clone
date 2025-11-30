from django.shortcuts import render
from .models import (
    CustomUser,
    AdminTeacher,
    Student,
    Course,
    CourseType
)
from .serializers import (
    CustomUserSerializer,
    AdminTeacherSerializer,
    StudentSerializer,
    CourseSerializer,
    CourseTypeSerializer
)




# Create your views here.
