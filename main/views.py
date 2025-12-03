from django.core.serializers import serialize
from django.shortcuts import render, get_list_or_404, get_object_or_404
from rest_framework import viewsets, mixins
from rest_framework.response import Response
from rest_framework import status

from rest_framework.permissions import BasePermission


from .models import (
    Weekday, Room, Attendence,
    Group, StudentGroup, Lesson,
    Homework, 
)
from .serializers import (
    WeekDaySerializer, RoomSerializer,
    AttendenceSerailizer, GroupSerializer,
    StudentGroupSerializer, LessonSerializer,
    HomeworkSerializer
)


from account.models import (
    CustomUser, AdminTeacher, Student,
    CourseType, Course
)
from account.serializers import (
    CourseSerializer, CourseTypeSerializer,
    AdminTeacherSerializer, StudentSerializer,
    CustomUserSerializer
)


# Create your views here.

# ADMIN

class AdminEnterPermission(BasePermission):
    def has_permission(self, request, view):
        return request.user and AdminTeacher.objects.filter(user__id = request.user.id).exists()
    
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


class AdminHomeView(viewsets.ViewSet):
    permission_classes = [AdminEnterPermission]

    def list(self, request):
        queryset = AdminTeacher.objects.select_related("user").all()
        data = AdminTeacherSerializer(queryset, many=True).data
        return Response(data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk):
        obj = get_object_or_404(AdminTeacher.objects.select_related("user"), pk=pk)
        data = AdminTeacherSerializer(obj).data
        return Response(data, status=status.HTTP_200_OK)

    def create(self, request):
        user_data = request.data.get("user")
        user_serializer = CustomUserSerializer(data=user_data)

        if not user_serializer.is_valid():
            return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        user = user_serializer.save()

        admin_data = request.data.copy()
        admin_data["user"] = user.id

        admin_serializer = AdminTeacherSerializer(data=admin_data)
        if not admin_serializer.is_valid():
            return Response(admin_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        admin = admin_serializer.save()
        return Response(
            {"message": "success", "data": AdminTeacherSerializer(admin).data},
            status=status.HTTP_201_CREATED
        )

    def update(self, request, pk):
        admin_instance = get_object_or_404(AdminTeacher, pk=pk)

        user = admin_instance.user
        user_data = request.data.get("user")

        partial = request.method == 'PATCH'

        user_serializer = CustomUserSerializer(user, data=user_data, partial=partial)
        if not user_serializer.is_valid():
            return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        user_serializer.save()

        admin_data = request.data.copy()
        admin_data["user"] = user.id

        admin_serializer = AdminTeacherSerializer(admin_instance, data=admin_data, partial=partial)
        if not admin_serializer.is_valid():
            return Response(admin_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        admin_serializer.save()

        return Response(admin_serializer.data, status=status.HTTP_202_ACCEPTED)

    def destroy(self, request, pk):
        admin_teacher = get_object_or_404(AdminTeacher, pk=pk)
        
        admin_teacher.delete()
        return Response({"message": "deleted"}, status=status.HTTP_204_NO_CONTENT)
    


