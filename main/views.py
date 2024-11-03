from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from .models import TestScore, School, Region, Student, StudentProfile, LearningPath
from django.db.models import Avg
import pandas as pd
import plotly.express as px
from django.http import HttpResponse
from .serializers import RegionSerializer, SchoolSerializer, StudentSerializer, TestScoreSerializer, StudentProfileSerializer, LearningPathSerializer
from django.db.models import Avg, Count, Sum
from django.shortcuts import render, get_object_or_404
 




class RegionViewSet(viewsets.ModelViewSet):
    queryset = Region.objects.all()
    serializer_class = RegionSerializer

class SchoolViewSet(viewsets.ModelViewSet):
    queryset = School.objects.all()
    serializer_class = SchoolSerializer

class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

class TestScoreViewSet(viewsets.ModelViewSet):
    queryset = TestScore.objects.all()
    serializer_class = TestScoreSerializer

class TestScoreChartDataView(viewsets.ViewSet):
    def list(self, request):
        # Aggregating average test scores by region
        scores_by_region = TestScore.objects.values('student__school__region__name').annotate(average_score=Avg('score'))

        # Create a structured response for chart.js or plotly
        data = {
            "labels": [item['student__school__region__name'] for item in scores_by_region],
            "data": [item['average_score'] for item in scores_by_region],
        }
        return Response(data)

def test_scores_plotly_view(request):
    return render(request, 'test_scores_plotly.html')
    
def student_list(request):
    students = Student.objects.all()
    return render(request, 'education/student_list.html', {'students': students})

def test_scores_plotly(request):
    
    return render(request, 'test_scores_plotly.html')


def export_students_excel(request):
    # Fetch student data from the database
    students = Student.objects.all().values('name', 'gender', 'school__name', 'enrolled', 'dropout')

    # Convert the queryset to a DataFrame
    df = pd.DataFrame(list(students))

    # Prepare HTTP response with the appropriate content type for Excel
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="students.xlsx"'

    # Write the DataFrame to an Excel file in the response
    df.to_excel(response, index=False)

    return response

def export_students_excel(request):
    students = Student.objects.all().values('name', 'gender', 'age', 'enrolled', 'dropout', 'school__name')
    df = pd.DataFrame(list(students))
    response = HttpResponse(content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="students.xlsx"'
    df.to_excel(response, index=False)
    return response


def dropout_chart(request):
    # Query to get the count of dropouts and enrolled students
    dropout_count = Student.objects.filter(dropout=True).count()
    enrolled_count = Student.objects.filter(dropout=False).count()

    # Data for the dropout chart
    dropout_data = {
        'Status': ['Enrolled', 'Dropped Out'],
        'Count': [enrolled_count, dropout_count]
    }

    # Create a Plotly pie chart for dropouts
    dropout_fig = px.pie(
        names=dropout_data['Status'],
        values=dropout_data['Count'],
        title='Dropout vs Enrolled Students'
    )
    dropout_chart = dropout_fig.to_html(full_html=False)

    # Query to get average test scores by subject
    # Update this line to correctly reference the subject name
    test_scores_data = TestScore.objects.values('lesson__subject__name').annotate(avg_score=Avg('score'))

    subjects = [data['lesson__subject__name'] for data in test_scores_data]
    avg_scores = [data['avg_score'] for data in test_scores_data]

    # Create a Plotly bar chart for test scores
    test_scores_fig = px.bar(
        x=subjects,
        y=avg_scores,
        title='Average Test Scores by Subject',
        labels={'x': 'Subject', 'y': 'Average Score'}
    )
    test_scores_chart = test_scores_fig.to_html(full_html=False)

    # Pass both charts to the template
    return render(request, 'combined_charts.html', {
        'dropout_chart': dropout_chart,
        'test_scores_chart': test_scores_chart
    })


def enrollment_comparison_chart(request):
    # Calculate enrollment rate for rural schools
    rural_schools = School.objects.filter(location='Rural')
    rural_enrolled = Student.objects.filter(school__in=rural_schools, enrolled=True).count()
    rural_total = Student.objects.filter(school__in=rural_schools).count()
    rural_rate = (rural_enrolled / rural_total) * 100 if rural_total else 0

    # Calculate enrollment rate for urban schools
    urban_schools = School.objects.filter(location='Urban')
    urban_enrolled = Student.objects.filter(school__in=urban_schools, enrolled=True).count()
    urban_total = Student.objects.filter(school__in=urban_schools).count()
    urban_rate = (urban_enrolled / urban_total) * 100 if urban_total else 0

    # Data for chart
    enrollment_data = {
        'Location': ['Rural', 'Urban'],
        'Enrollment Rate (%)': [rural_rate, urban_rate]
    }

    # Create a Plotly bar chart
    import plotly.express as px
    fig = px.bar(x=enrollment_data['Location'], y=enrollment_data['Enrollment Rate (%)'],
                 title='School Enrollment Rates in Rural and Urban Areas',
                 labels={'x': 'Location', 'y': 'Enrollment Rate (%)'})
    
    enrollment_chart = fig.to_html(full_html=False)

    return render(request, 'enrollment_comparison_chart.html', {
        'enrollment_chart': enrollment_chart,
    })
    
def education_metrics_view(request):
    # Total Students
    total_students = Student.objects.count()

    # Enrolled Students
    enrolled_students = Student.objects.filter(enrolled=True).count()

    # Dropout Students
    dropout_students = Student.objects.filter(dropout=True).count()

    # Enrollment Rate
    enrollment_rate = (enrolled_students / total_students) * 100 if total_students > 0 else 0

    # Dropout Rate
    dropout_rate = (dropout_students / total_students) * 100 if total_students > 0 else 0

    # Average Performance
    average_performance = TestScore.objects.aggregate(avg_score=Avg('score'))['avg_score'] or 0

    # Performance by Subject
    performance_by_subject = TestScore.objects.values('lesson__subject__name').annotate(avg_score=Avg('score')).order_by('lesson__subject__name')
    context = {
        'total_students': total_students,
        'enrolled_students': enrolled_students,
        'enrollment_rate': enrollment_rate,
        'dropout_rate': dropout_rate,
        'average_performance': average_performance,
        'performance_by_subject': performance_by_subject,
    }

    return render(request, 'education/metrics.html', context)



    # update

    # 1. StudentProfile ViewSet
class StudentProfileViewSet(viewsets.ModelViewSet):
    queryset = StudentProfile.objects.all()
    serializer_class = StudentProfileSerializer


# 2. LearningPath ViewSet
class LearningPathViewSet(viewsets.ModelViewSet):
    queryset = LearningPath.objects.all()
    serializer_class = LearningPathSerializer


# 3. TestScore ViewSet
class TestScoreViewSet(viewsets.ModelViewSet):
    queryset = TestScore.objects.all()
    serializer_class = TestScoreSerializer


# 4. View to display Learning Path for a specific student
def student_learning_path(request, student_id):
    student_profile = get_object_or_404(StudentProfile, id=student_id)
    learning_path = LearningPath.objects.filter(student=student_profile)

    return render(request, 'education/student_learning_path.html', {
        'student_profile': student_profile,
        'learning_path': learning_path,
    })


# 5. View to display Test Scores for a specific student
def student_test_scores(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    test_scores = TestScore.objects.filter(student=student)

    return render(request, 'education/student_test_scores.html', {
        'student': student,
        'test_scores': test_scores,
    })


# 6. View to display the average test score for a student
def average_test_score(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    average_score = TestScore.objects.filter(student=student).aggregate(Avg('score'))['score__avg']

    return render(request, 'education/student_average_score.html', {
        'student': student,
        'average_score': average_score,
    })
    
    from django.shortcuts import render, get_object_or_404
from .models import Student

def student_detail(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    test_scores = TestScore.objects.filter(student=student).select_related('lesson')  # Preload lesson data
    
    # Prepare context to pass to the template
    context = {
        'student': student,
        'test_scores': test_scores,
    }
    
    return render(request, 'Education/student_detail.html', context)


def students_by_school_view(request, school_id):
    # Fetch students who belong to a specific school
    students = Student.objects.filter(school__id=school_id)

    # Render the template with the filtered students
    return render(request, 'education/students_by_school.html', {'students': students})


def student_profile_view(request, user_id):
    # Fetch the student's profile based on the User's ID
    student_profile = get_object_or_404(StudentProfile, user__id=user_id)

    # Render the template with the profile data
    return render(request, 'education/student_profile.html', {'student_profile': student_profile})
