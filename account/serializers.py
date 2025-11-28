from rest_framework import serializers
from .models import (
    CustomUser,
    CourseType,
    Course,
    AdminTeacher,
    Student,
)
from main.models import Group
from main.serializers import (
    AttendenceSerailizer,
    HomeworkSerializer,
    LessonSerializer,
    StudentGroupSerializer,
    GroupSerializer,
    RoomSerializer,
    WeekDaySerializer
)

class StudentSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        queryset=CustomUser.phone.all(),
        read_only=True,
    )
    groups = StudentGroupSerializer(source='groups', many=True, read_only=True)


    class Meta:
        model = Student
        fields = '__all__'
        read_only_fields = ['id', 'xp', 'coins', 'level', 'is_active']




class AdminTeacherSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        queryset=CustomUser.phone.all(),
        read_only=True,
    )


    class Meta:
       model = AdminTeacher
       fields = '__all__'
       read_only_fields = ['id', 'is_active']


class CustomUserSerializer(serializers.ModelSerializer):
    students = StudentSerializer(many=True, read_only=True)
    admin_teachers = AdminTeacherSerializer(many=True, read_only=True)
    profession = serializers.CharField(max_length=100, required=False)
    image = serializers.ImageField(required=False)

    class Meta:
        model = CustomUser
        fields = [
            "id", "phone", "first_name", "last_name",
            "profession", "image", "fullname"
        ]
        read_only_fields = ['id']


class CourseSerializer(serializers.ModelSerializer):
    admin_teachers = AdminTeacherSerializer(many=True, read_only=True)
    course_type = serializers.PrimaryKeyRelatedField(
        queryset=CourseType.objects.all()
    )

    class Meta:
        model = Course
        fields = '__all__'
        read_only_fields = ['id', 'is_active']


class CourseTypeSerializer(serializers.ModelSerializer):
    courses = CourseSerializer(many=True, read_only=True)

    class Meta:
        model = CourseType
        fields = ['name']


