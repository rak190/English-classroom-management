from django.urls import path
from . import views

app_name = 'management'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('register/', views.register_teacher, name='register_teacher'),
    path('students/', views.student_list, name='student_list'),
    path('students/add/', views.student_create, name='student_create'),
    path('students/<int:student_id>/edit/', views.student_edit, name='student_edit'),
    path('students/<int:student_id>/delete/', views.student_delete, name='student_delete'),
    path('students/import/', views.student_bulk_import, name='student_bulk_import'),
    path('classes/', views.class_list, name='class_list'),
    path('classes/add/', views.class_create, name='class_create'),
    path('classes/<int:course_id>/', views.class_detail, name='class_detail'),
    path('classes/<int:course_id>/edit/', views.class_edit, name='class_edit'),
    path('classes/<int:course_id>/delete/', views.class_delete, name='class_delete'),
    path('classes/<int:course_id>/enroll/', views.class_bulk_enroll, name='class_bulk_enroll'),
    path('classes/<int:course_id>/remove/<int:student_id>/', views.remove_student_from_class, name='remove_student_from_class'),
    path('attendance/', views.attendance_view, name='attendance_view'),
    path('attendance/bulk/', views.bulk_attendance_view, name='bulk_attendance_view'),
    path('homework/', views.homework_view, name='homework_view'),
    path('homework/<int:submission_id>/edit-status/', views.homework_status_edit, name='homework_status_edit'),
    path('scores/', views.score_view, name='score_view'),
    path('scores/bulk/', views.bulk_score_entry_view, name='bulk_score_entry_view'),
    path('materials/', views.material_view, name='material_view'),
    path('schedule/', views.schedule_view, name='schedule_view'),
    path('progress/', views.progress_tracking_view, name='progress_tracking_view'),
    path('students/<int:student_id>/report/', views.parent_report_view, name='parent_report_view'),
    
    # AI Tools
    path('ai/', views.ai_dashboard_view, name='ai_dashboard'),
    path('ai/worksheet/', views.worksheet_generator_view, name='ai_worksheet'),
    path('ai/lesson-plan/', views.lesson_plan_generator_view, name='ai_lesson_plan'),
    path('ai/test/', views.test_generator_view, name='ai_test'),
    path('setup/', views.setup_database, name='setup_database'),
]
