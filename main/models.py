from django.db import models

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

class Student(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]
    name = models.CharField(max_length=200)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    age = models.IntegerField()
    enrolled = models.BooleanField(default=True)
    dropout = models.BooleanField(default=False)
    school = models.ForeignKey(School, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class TestScore(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject = models.CharField(max_length=100)
    score = models.FloatField()

    def __str__(self):
        return f"{self.student.name} - {self.subject}"
