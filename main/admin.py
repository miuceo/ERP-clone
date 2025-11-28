from django.contrib import admin
from unfold.admin import ModelAdmin
from import_export.admin import ImportExportModelAdmin
from .models import (
    Weekday,
    Room,
    Group,
    StudentGroup,
    Lesson,
    Homework,
    Attendence
)

# Register your models here.


@admin.register(Weekday)
class WeekdayModelAdmin(ModelAdmin):
    list_display =  ['name']
    search_fields = ['name']


@admin.register(Room)
class RoomModelAdmin(ModelAdmin):
    list_display =  ['name']
    search_fields = ['name']


@admin.register(Group)
class GroupModelAdmin(ModelAdmin, ImportExportModelAdmin):
    list_display =  ['name', 'course', 'teacher', 'room']
    list_display_links = ['name', 'course', 'teacher', 'room']
    list_filter = ['course', 'teacher', 'days']
    search_fields = ['name', 'course', 'teacher', 'room']
    ordering = ['-end_date']


@admin.register(StudentGroup)
class StudentGroupModelAdmin(ModelAdmin, ImportExportModelAdmin):
    list_display =  ['student', 'group', 'status']
    list_display_links = ['student', 'group', 'status']
    list_filter = ['student', 'group', 'status']
    search_fields = ['student', 'group', 'status']
    ordering = ['-left_at']


@admin.register(Lesson)
class LessonModelAdmin(ModelAdmin, ImportExportModelAdmin):
    list_display =  ['name', 'group', 'day']
    list_display_links = ['name', 'group', 'day']
    list_filter = ['group', 'day']
    search_fields = ['name', 'group', 'day', 'task_file', 'task_text']


@admin.register(Homework)
class HomeworkModelAdmin(ModelAdmin, ImportExportModelAdmin):
    list_display = ['student', 'group', 'lesson', 'status']
    list_display_links = ['student', 'group', 'lesson', 'status']
    list_filter = ['student', 'lesson', 'group', 'status']
    search_fields = ['student', 'group', 'lesson', 'status', 'text']
    ordering = ['-time']


@admin.register(Attendence)
class AttendenceModelAdmin(ModelAdmin, ImportExportModelAdmin):
    list_display =  ['student', 'lesson', 'status']
    list_display_links = ['student', 'lesson', 'status']
    list_filter = ['student', 'lesson', 'status']
    search_fields = ['student', 'lesson', 'status']
    ordering = ['-time']
