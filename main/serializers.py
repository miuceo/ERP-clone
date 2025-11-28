from rest_framework import serializers
from rest_framework.validators import qs_exists

from account.models import Student, AdminTeacher, Course
from account.serializers import StudentSerializer, AdminTeacherSerializer
from .models import (
    Weekday,
    Room,
    Group,
    StudentGroup,
    Lesson,
    Homework,
    Attendence,
)


class AttendenceSerailizer(serializers.ModelSerializer):
    student = serializers.PrimaryKeyRelatedField(
        queryset=Student.objects.all()
    )
    lesson = serializers.PrimaryKeyRelatedField(
        queryset=Lesson.objects.all()
    )

    class Meta:
        model = Attendence
        fields = '__all__'
        read_only_fields = ['id', 'time']


class HomeworkSerializer(serializers.ModelSerializer):
    lesson = serializers.PrimaryKeyRelatedField(
        queryset=Lesson.objects.all()
    )
    student = serializers.PrimaryKeyRelatedField(
        queryset=Student.objects.all()
    )
    group = serializers.PrimaryKeyRelatedField(
        queryset=Group.objects.all()
    )

    class Meta:
        model = Homework
        fields = '__all__'
        read_only_fields = ['id', 'time', 'xp', 'coins', 'status']


class LessonSerializer(serializers.ModelSerializer):
    group = serializers.PrimaryKeyRelatedField(
        queryset=Group.objects.all()
    )
    homeworks = HomeworkSerializer(source='homeworks', many=True, read_only=True)
    attendences = AttendenceSerailizer(source='attendences', many=True, read_only=True)

    class Meta:
        model = Lesson
        fields = '__all__'
        read_only_fields = ['id']


class StudentGroupSerializer(serializers.ModelSerializer):
    student = serializers.PrimaryKeyRelatedField(
        queryset=Student.objects.all()
    )
    group = serializers.PrimaryKeyRelatedField(
        queryset=Group.objects.all()
    )

    class Meta:
        model = StudentGroup
        fields = '__all__'
        read_only_fields = ['id', 'joined_at', 'left_at', 'status']


class GroupSerializer(serializers.ModelSerializer):
    teacher = serializers.PrimaryKeyRelatedField(
        queryset=AdminTeacher.objects.all()
    )
    room = serializers.PrimaryKeyRelatedField(
        queryset=Room.objects.all()
    )
    course = serializers.PrimaryKeyRelatedField(
        queryset=Course.objects.all()
    )
    students = StudentSerializer(source = 'students',many=True, read_only=True)
    teachers = AdminTeacherSerializer(source='admin_teachers', many=True, read_only=True)
    lessons = LessonSerializer(source='lessons', many=True, read_only=True)
    homeworks = HomeworkSerializer(source='homeworks')

    class Meta:
        model = Group
        fields = '__all__'
        read_only_fields = ['id', 'start_date', 'end_date', 'start_time', 'end_time', 'days']


class RoomSerializer(serializers.ModelSerializer):
    groups = GroupSerializer(source='groups', many=True, read_only=True)

    class Meta:
        model = Room
        fields = ['name']


class WeekDaySerializer(serializers.ModelSerializer):
    groups = GroupSerializer(source='groups', many=True, read_only=True)

    class Meta:
        model = Weekday
        fields = ['name']
