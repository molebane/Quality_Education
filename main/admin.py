from django.contrib import admin
from .models import Region, School, Student, TestScore, StudentProfile, LearningPath, TestScore
from import_export.admin import ImportExportModelAdmin
from import_export import resources

# Register Region and School models
admin.site.register(Region)
admin.site.register(School)

# Define the resource class for Student import/export
class StudentResource(resources.ModelResource):
    class Meta:
        model = Student

# Register Student with ImportExportModelAdmin
@admin.register(Student)
class StudentAdmin(ImportExportModelAdmin):
    resource_class = StudentResource
    list_display = ('name', 'gender', 'age', 'enrolled', 'dropout', 'school')
    search_fields = ['name']

# Register TestScore model
admin.site.register(TestScore)


# update


class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'school', 'learning_level', 'current_subject')
    search_fields = ('user__username', 'school__name', 'current_subject__name')
    list_filter = ('school', 'learning_level')

# Register LearningPath Model
@admin.register(LearningPath)
class LearningPathAdmin(admin.ModelAdmin):
    list_display = ('student', 'lesson', 'completed')
    search_fields = ('student__user__username', 'lesson__title')
    list_filter = ('completed', 'lesson__subject')

# Register TestScore Model
@admin.register(TestScore)
class TestScoreAdmin(admin.ModelAdmin):
    list_display = ('student', 'lesson', 'score')
    search_fields = ('student__name', 'lesson__title')
    list_filter = ('lesson__subject', 'score')