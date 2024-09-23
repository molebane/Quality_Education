from django.contrib import admin
from .models import Region, School, Student, TestScore
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
