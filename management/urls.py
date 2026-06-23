from django.urls import path
from . import views

app_name = 'management'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('students/', views.student_list, name='student_list'),
    path('students/add/', views.student_create, name='student_create'),
    path('classes/', views.class_list, name='class_list'),
    path('classes/<int:course_id>/', views.class_detail, name='class_detail'),
    path('attendance/', views.attendance_view, name='attendance_view'),
    path('homework/', views.homework_view, name='homework_view'),
    path('scores/', views.score_view, name='score_view'),
    path('materials/', views.material_view, name='material_view'),
    path('schedule/', views.schedule_view, name='schedule_view'),
    path('progress/', views.progress_tracking_view, name='progress_tracking_view'),
    path('students/<int:student_id>/report/', views.parent_report_view, name='parent_report_view'),
    
    # AI Tools
    path('ai/', views.ai_dashboard_view, name='ai_dashboard'),
    path('ai/worksheet/', views.worksheet_generator_view, name='ai_worksheet'),
    path('ai/lesson-plan/', views.lesson_plan_generator_view, name='ai_lesson_plan'),
    path('ai/test/', views.test_generator_view, name='ai_test'),
]
