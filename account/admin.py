from django.contrib import admin
from unfold.admin import ModelAdmin
from import_export.admin import ImportExportModelAdmin
from .models import CustomUser, CourseType, Course, AdminTeacher, Student

# Register your models here.

@admin.register(CustomUser)
class CustomUserAdmin(ImportExportModelAdmin, ModelAdmin):
    model = CustomUser

    list_display = ('phone', 'fullname', 'email', 'is_staff', 'is_active', 'is_superuser')
    search_fields = ('phone', 'fullname', 'email')
    ordering = ('phone',)

    fieldsets = (
        ('Asosiy ma\'lumotlar', {
            'fields': ('phone', 'password', 'email', 'first_name', 'last_name', 'profession', 'image'),
        }),
        ('Ruxsatlar', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        ('Tizim ma\'lumotlari', {
            'fields': ('last_login', 'date_joined'),
        })
    )

    add_fieldsets = (
        ('Yangi foydalanuvchi', {
            'classes': ('wide',),
            'fields': (
                'phone', 'email', 'first_name', 'last_name',
                'profession', 'image',
                'password',
                'is_staff', 'is_superuser'
            ),
        }),
    )

@admin.register(CourseType)
class CourseTypeModelAdmin(ModelAdmin, ImportExportModelAdmin):
    list_display = ['name']
    search_fields = ['name']


@admin.register(Course)
class CourseModelAdmin(ModelAdmin, ImportExportModelAdmin):
    list_display = ['name', 'price', 'course_type']
    list_display_links = ['name', 'price', 'course_type']
    list_filter = ['price', 'course_type']
    search_fields = ['name', 'price', 'course_type']
    ordering = ['-price']


@admin.register(AdminTeacher)
class AdminTeacherModelAdmin(ModelAdmin, ImportExportModelAdmin):
    list_display =  ['user', 'role', 'course', 'is_active']
    list_display_links = ['user', 'role', 'course', 'is_active']
    list_filter = ['role', 'course', 'is_active']
    search_fields = ['user', 'role', 'course', 'is_active']


@admin.register(Student)
class StudentModelAdmin(ModelAdmin, ImportExportModelAdmin):
    list_display =  ['user', 'gender', 'year', 'level', 'xp', 'coins', 'is_active']
    list_display_links = ['user', 'gender', 'level', 'year', 'xp', 'coins', 'is_active']
    list_filter = ['gender', 'year', 'level', 'xp', 'is_active']
    search_fields = ['user']
    ordering = ['-level']




