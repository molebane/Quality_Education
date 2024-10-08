from django.db import models
from django.contrib.auth.models import User

class Region(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class School(models.Model):
    SCHOOL_LOCATION_CHOICES = [
        ('Rural', 'Rural'),
        ('Urban', 'Urban'),
    ]
    
    name = models.CharField(max_length=200)
    capacity = models.IntegerField()
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    location = models.CharField(max_length=5, choices=SCHOOL_LOCATION_CHOICES)

    def __str__(self):
        return self.name

class Subject(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name

class Lesson(models.Model):
    title = models.CharField(max_length=100)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    content = models.TextField()
    difficulty_level = models.IntegerField(default=1)

    def __str__(self):
        return self.title

class Student(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]
    name = models.CharField(max_length=200)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    age = models.IntegerField()
    enrolled = models.BooleanField(default=True)
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    dropout = models.BooleanField(default=False)

    def __str__(self):
        return self.name
class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    current_subject = models.ForeignKey(Subject, on_delete=models.SET_NULL, null=True, blank=True)
    learning_level = models.IntegerField(default=1)
    school = models.ForeignKey(School, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

class LearningPath(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.student.user.username} - {self.lesson.title}'

class TestScore(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    score = models.FloatField()

    def __str__(self):
        return f"{self.student.name} - {self.lesson.title} ({self.score})"
