# serializers.py
from rest_framework import serializers
from .models import Region, School, Student, TestScore

class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = '__all__'

class SchoolSerializer(serializers.ModelSerializer):
    class Meta:
        model = School
        fields = '__all__'

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'

class TestScoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestScore
        fields = '__all__'
