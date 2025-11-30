from rest_framework import serializers
from .models import CustomUser, Course, CourseType, AdminTeacher, Student


class StudentSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        queryset=CustomUser.objects.all(),
    )

    class Meta:
        model = Student
        fields = '__all__'
        read_only_fields = ['id', 'xp', 'coins', 'level', 'is_active']


class AdminTeacherSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        queryset=CustomUser.objects.all(),
    )


    class Meta:
        model = AdminTeacher
        fields = '__all__'
        read_only_fields = ['id', 'is_active',]




class CustomUserSerializer(serializers.ModelSerializer):
    profession = serializers.CharField(max_length=100, required=False)
    image = serializers.ImageField(required=False)
    password = serializers.CharField(write_only=True, required=False)


    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'profession', 'image', 'phone', 'password', 'is_active']
        read_only_fields = ['id']
        
    def validate_password(self, password):
        
        if not len(password) >= 8:
            raise serializers.ValidationError("The password must contain at least 8 characters")
        
        min_char, up_char, num, misc = 0, 0, 0, 0
        for i in str(password):
            if i.isdigit():
                num+=1
            if i.isupper():
                up_char+=1
            if i.islower():
                min_char+=1
            else:
                misc+=1
                
        if not (min_char>=1 and up_char>=1 and num>=1 and misc>=1):
            raise serializers.ValidationError("The password must contain at least 1 upper character, 1 lower chracter, 1 numiric character, 1 something else!")
        
        return password

    def validate_phone(self, phone):
        if not (phone.startswith('+998') or phone.startswith('998')):
            raise serializers.ValidationError("Phone must start with +998 or 998")
        
        if phone.startswith('+998'):
            if not (len(phone[1:])==12 and phone.isdigit()):
                raise serializers.ValidationError("Phone must have 12 characters and all characters must be numeric!")
        if phone.startswith('998'):
            if not (len(phone)==12 and phone.isdigit()):
                raise serializers.ValidationError("Phone must have 12 characters and all characters must be numeric!")
        
        return phone
    
    def validate_email(self, email):
        if not len(email.split('@')[0]) >= 5 or not((email.split('@')[0].isdigit() or email.split('@')[0].isalpha()) and email.split('@')[0][0].isalpha()):
            raise serializers.ValidationError("Please enter email properly")
        if not email.endswith(('gmail.com', 'yahoo.com', 'yandex.ru', 'mail.ru')):
            raise serializers.ValidationError('The email must end with gmail.com, yahoo.com, yandex.ru, mail.ru')
        
        return email
    
    def validate(self, attrs):
                    



class CourseSerializer(serializers.ModelSerializer):
    course_type = serializers.PrimaryKeyRelatedField(
        queryset=CourseType.objects.all()
    )

    class Meta:
        model = Course
        fields = '__all__'
        read_only_fields = ['id', 'is_active']


class CourseTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = CourseType
        fields = ['name']