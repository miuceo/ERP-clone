from django.core.validators import MaxValueValidator
from django.db import models

# Create your models here.

class Weekday(models.Model):
    name = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'weekday'
        verbose_name_plural = 'weekdays'
        db_table = 'weekday'


class Room(models.Model):
    name = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'room'
        verbose_name_plural = 'rooms'
        db_table = 'room'


class Group(models.Model):
    name = models.CharField(max_length=20, unique=True)
    course = models.ForeignKey('account.Course', on_delete=models.SET_NULL, related_name='groups', null=True, blank=True)
    teacher = models.ForeignKey('account.AdminTeacher', on_delete=models.SET_NULL, related_name='groups', null=True, blank=True)
    start_date = models.DateField()
    end_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    room = models.ForeignKey(Room, on_delete=models.SET_NULL, null=True, related_name='groups', blank=True)
    days = models.ManyToManyField("main.Weekday")

    def __str__(self):
        return f'{self.name} - {self.start_time} - {self.end_time} - {self.room.name}'

    class Meta:
        verbose_name = 'group'
        verbose_name_plural = 'groups'
        db_table = 'group'


class StudentGroup(models.Model):
    STATUS = (
        ('active', 'Active'),
        ('left', 'Left'),
        ('finished', 'Finished'),
    )

    student = models.ForeignKey('account.Student', on_delete=models.CASCADE, related_name='groups')
    group = models.ForeignKey('main.Group', on_delete=models.CASCADE, related_name='students')
    joined_at = models.DateField(auto_now_add=True)
    left_at = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS, default='active')

    def __str__(self):
        return f'{self.student.fullname} - {self.group.name}'

    class Meta:
        verbose_name = 'student_group'
        verbose_name_plural = 'student_groups'
        db_table = 'student_group'


def lesson_video_path(instance, filename):
    instance_group_name = instance.group.name.replace(" ", "_")
    return f'lessons/{instance_group_name}/videos/'

def lesson_file_path(instance, filename):
    instance_group_name = instance.group.name.replace(" ", "_")
    return f'lessons/{instance_group_name}/files/'

class Lesson(models.Model):
    name = models.CharField(max_length=100)
    group = models.ForeignKey('main.Group', on_delete=models.CASCADE, related_name='lessons')
    video = models.FileField(upload_to=lesson_video_path, null=True)
    task_text = models.TextField()
    task_file = models.FileField(upload_to=lesson_file_path)
    day = models.ForeignKey('main.Weekday', on_delete=models.SET_NULL, related_name='lessons', null=True, blank=True)

    def __str__(self):
        return f'{self.name} - {self.group.course.name} - {self.group.name} - {self.group.room} - {self.group.start_time} - {self.group.end_time}'

    class Meta:
        verbose_name = 'lesson'
        verbose_name_plural = 'lessons'
        db_table = 'lesson'


def homework_file_path(instance, filename):
    student_name = instance.student.fullname.replace(" ", "_")
    group_name = instance.group.name.replace(" ", "_")
    return f'homeworks/{student_name}/{group_name}/{filename}'

class Homework(models.Model):
    HOMEWORK_STATUS = (
        ('not_given', 'NOT GIVEN'),
        ('not_done', 'NOT DONE'),
        ('waiting', 'WAITING'),
        ('done', 'DONE'),
        ('refused', 'REFUSED'),
    )

    lesson = models.ForeignKey('main.Lesson', on_delete=models.CASCADE, related_name='homeworks')
    student = models.ForeignKey('account.Student', on_delete=models.CASCADE, related_name='homeworks')
    group = models.ForeignKey('main.Group', on_delete=models.CASCADE, related_name='homeworks')
    text = models.TextField()
    answer = models.TextField(null=True, blank=True)
    ball = models.PositiveBigIntegerField(validators=[MaxValueValidator(100)], default=0)
    file = models.FileField(upload_to=homework_file_path)
    xp = models.PositiveIntegerField(default=0)
    coins = models.PositiveIntegerField(default=0)
    time = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=HOMEWORK_STATUS)

    def __str__(self):
        return f'{self.student.fullname} - {self.group.name} - {self.lesson.name} - {self.status}'

    class Meta:
        verbose_name = 'homework'
        verbose_name_plural = 'homeworks'
        db_table = 'homework'
        ordering = ['-time']



class Attendence(models.Model):
    ATTENDENCE_STATUS  = (
        ("came", "CAME"),
        ("absent", "ABSENT"),
        ("late", "LATE")
    )

    student = models.ForeignKey('account.Student', on_delete=models.CASCADE, related_name='attendences')
    lesson = models.ForeignKey('main.Lesson', on_delete=models.CASCADE, related_name='attendences')
    time = models.TimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=ATTENDENCE_STATUS)

    def __str__(self):
        return f'{self.student.fullname} - {self.lesson.name} - {self.status}'

    class Meta:
        unique_together = ('student', 'lesson')
        verbose_name = 'attendence'
        verbose_name_plural = 'attendences'
        db_table = 'attendence'

