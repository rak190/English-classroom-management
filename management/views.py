from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.core.management import call_command
from django.contrib.auth.models import User
from django.db.utils import OperationalError
import traceback
import csv
from datetime import datetime
from django.db.models import Count, Avg
from .models import Student, Course, Enrollment, Attendance, Homework, HomeworkSubmission, Score, Material
from .forms import StudentForm, CourseForm, AttendanceForm, MaterialForm

@login_required
def dashboard(request):
    total_students = Student.objects.count()
    active_classes = Course.objects.count()
    
    # Simple placeholder logic for dashboard stats for Phase 1
    # In a real app, this would filter by today's date
    today_attendance_present = Attendance.objects.filter(status='Present').count()
    today_attendance_total = Attendance.objects.count()
    
    hw_submitted = HomeworkSubmission.objects.filter(status='Submitted').count()
    hw_total = HomeworkSubmission.objects.count()

    context = {
        'total_students': total_students,
        'active_classes': active_classes,
        'today_attendance_present': today_attendance_present,
        'today_attendance_total': today_attendance_total,
        'hw_submitted': hw_submitted,
        'hw_total': hw_total,
    }
    return render(request, 'management/dashboard.html', context)

@login_required
def student_list(request):
    students = Student.objects.all().order_by('-join_date')
    return render(request, 'management/student_list.html', {'students': students})

@login_required
def student_create(request):
    if request.method == 'POST':
        form = StudentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('management:student_list')
    else:
        form = StudentForm()
    return render(request, 'management/student_form.html', {'form': form})

@login_required
def class_list(request):
    courses = Course.objects.annotate(student_count=Count('enrollments')).all()
    return render(request, 'management/class_list.html', {'courses': courses})

@login_required
def class_detail(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    enrollments = course.enrollments.all()
    return render(request, 'management/class_detail.html', {'course': course, 'enrollments': enrollments})

@login_required
def attendance_view(request):
    if request.method == 'POST':
        form = AttendanceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('management:attendance_view')
    else:
        form = AttendanceForm()
        
    attendances = Attendance.objects.all().order_by('-date')
    return render(request, 'management/attendance.html', {'form': form, 'attendances': attendances})

@login_required
def homework_view(request):
    submissions = HomeworkSubmission.objects.all().select_related('student', 'homework')
    return render(request, 'management/homework.html', {'submissions': submissions})

@login_required
def score_view(request):
    scores = Score.objects.all().select_related('student', 'course')
    
    # Calculate average scores
    student_averages = Score.objects.values('student__name').annotate(average=Avg('value'))
    
    return render(request, 'management/scores.html', {
        'scores': scores,
        'student_averages': student_averages
    })

@login_required
def material_view(request):
    if request.method == 'POST':
        form = MaterialForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('management:material_view')
    else:
        form = MaterialForm()
        
    materials = Material.objects.all().order_by('-uploaded_at')
    return render(request, 'management/materials.html', {'form': form, 'materials': materials})

@login_required
def schedule_view(request):
    from .models import Schedule
    schedules = Schedule.objects.all().select_related('course').order_by('day', 'start_time')
    
    # Group schedules by day for easier rendering in template
    days = ['MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT', 'SUN']
    schedule_by_day = {day: [] for day in days}
    for s in schedules:
        schedule_by_day[s.day].append(s)
        
    return render(request, 'management/schedule.html', {'schedule_by_day': schedule_by_day})

@login_required
def progress_tracking_view(request):
    # This view will gather overall data for charts
    courses = Course.objects.all()
    # Simple aggregation: Average score per course
    course_averages = Score.objects.values('course__class_name').annotate(average=Avg('value'))
    
    return render(request, 'management/progress.html', {
        'courses': courses,
        'course_averages': list(course_averages)
    })

@login_required
def parent_report_view(request, student_id):
    student = get_object_or_404(Student, pk=student_id)
    
    # Calculate attendance rate
    total_attendance = Attendance.objects.filter(student=student).count()
    present_attendance = Attendance.objects.filter(student=student, status='Present').count()
    attendance_rate = (present_attendance / total_attendance * 100) if total_attendance > 0 else 0
    
    # Get recent scores
    recent_scores = Score.objects.filter(student=student).order_by('-id')[:5]
    avg_score = Score.objects.filter(student=student).aggregate(Avg('value'))['value__avg'] or 0
    
    # Missing homework
    missing_hw = HomeworkSubmission.objects.filter(student=student, status='Not Submitted')
    
    context = {
        'student': student,
        'attendance_rate': round(attendance_rate, 1),
        'recent_scores': recent_scores,
        'avg_score': round(avg_score, 1),
        'missing_hw': missing_hw,
    }
    return render(request, 'management/parent_report.html', context)

import markdown
from . import ai_utils

@login_required
def ai_dashboard_view(request):
    return render(request, 'management/ai_dashboard.html')

@login_required
def ai_test_generator(request):
    return render(request, 'management/ai_test.html')

def setup_database(request):
    """A helper view to automatically run migrations and create a superuser for Vercel deployments"""
    output = []
    try:
        output.append("Starting database migrations...")
        call_command('migrate', interactive=False)
        output.append("Migrations completed successfully.")
        
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
            output.append("Superuser 'admin' created with password 'admin123'.")
        else:
            output.append("Superuser 'admin' already exists.")
            
        output.append("Setup complete! You can now go to /accounts/login/ and login with admin / admin123")
        return HttpResponse("<br>".join(output))
    except Exception as e:
        output.append("ERROR OCCURRED:")
        output.append(str(e))
        output.append(traceback.format_exc().replace('\n', '<br>'))
        return HttpResponse("<br>".join(output), status=500)

@login_required
def worksheet_generator_view(request):
    result_html = ""
    if request.method == 'POST':
        topic = request.POST.get('topic')
        level = request.POST.get('level')
        questions_count = request.POST.get('questions_count')
        
        markdown_result = ai_utils.generate_worksheet(topic, level, questions_count)
        result_html = markdown.markdown(markdown_result)
        
    return render(request, 'management/ai_worksheet.html', {'result_html': result_html})

@login_required
def lesson_plan_generator_view(request):
    result_html = ""
    if request.method == 'POST':
        topic = request.POST.get('topic')
        level = request.POST.get('level')
        duration = request.POST.get('duration')
        
        markdown_result = ai_utils.generate_lesson_plan(topic, level, duration)
        result_html = markdown.markdown(markdown_result)
        
    return render(request, 'management/ai_lesson_plan.html', {'result_html': result_html})

@login_required
def test_generator_view(request):
    result_html = ""
    if request.method == 'POST':
        test_type = request.POST.get('test_type')
        level = request.POST.get('level')
        topics = request.POST.get('topics')
        
        markdown_result = ai_utils.generate_test(test_type, topics, level)
        result_html = markdown.markdown(markdown_result)
        
    return render(request, 'management/ai_test.html', {'result_html': result_html})

@login_required
def student_bulk_import(request):
    if request.method == 'POST':
        if 'csv_file' not in request.FILES:
            return render(request, 'management/student_bulk_import.html', {'error': 'No file uploaded.'})
        
        csv_file = request.FILES['csv_file']
        if not csv_file.name.endswith('.csv'):
            return render(request, 'management/student_bulk_import.html', {'error': 'Please upload a valid CSV file.'})
            
        try:
            file_data = csv_file.read().decode('utf-8-sig').splitlines()
            reader = csv.DictReader(file_data)
            
            students_to_create = []
            for row in reader:
                if not row.get('student_id') or not row.get('name') or not row.get('parent_phone'):
                    continue
                
                if Student.objects.filter(student_id=row['student_id']).exists():
                    continue
                    
                join_date_str = row.get('join_date', '')
                try:
                    join_date = datetime.strptime(join_date_str, '%Y-%m-%d').date()
                except ValueError:
                    join_date = datetime.now().date()
                    
                students_to_create.append(Student(
                    student_id=row['student_id'],
                    name=row['name'],
                    gender=row.get('gender', 'O')[:1].upper(),
                    grade=row.get('grade', 'Unassigned'),
                    phone=row.get('phone', ''),
                    parent_phone=row['parent_phone'],
                    join_date=join_date
                ))
            
            if students_to_create:
                Student.objects.bulk_create(students_to_create)
                return render(request, 'management/student_bulk_import.html', {'success': f'Successfully imported {len(students_to_create)} students!'})
            else:
                return render(request, 'management/student_bulk_import.html', {'error': 'No new students imported. Make sure student_ids are unique and required columns are present.'})
                
        except Exception as e:
            return render(request, 'management/student_bulk_import.html', {'error': f'Error processing file: {str(e)}'})
            
    if 'download_template' in request.GET:
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="student_import_template.csv"'
        writer = csv.writer(response)
        writer.writerow(['student_id', 'name', 'gender', 'grade', 'parent_phone', 'phone', 'join_date'])
        writer.writerow(['STU-1001', 'Sok Dara', 'M', 'Grade 8', '012345678', '098765432', '2025-09-01'])
        writer.writerow(['STU-1002', 'Meas Bopha', 'F', 'Grade 8', '012345679', '', '2025-09-01'])
        return response
        
    return render(request, 'management/student_bulk_import.html')

@login_required
def class_bulk_enroll(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    enrolled_student_ids = course.enrollments.values_list('student_id', flat=True)
    available_students = Student.objects.exclude(id__in=enrolled_student_ids).order_by('name')
    
    if request.method == 'POST':
        selected_student_ids = request.POST.getlist('students')
        enrollments_to_create = []
        for s_id in selected_student_ids:
            enrollments_to_create.append(Enrollment(student_id=s_id, course=course))
            
        if enrollments_to_create:
            Enrollment.objects.bulk_create(enrollments_to_create)
            return redirect('management:class_detail', course_id=course.id)
            
    return render(request, 'management/class_bulk_enroll.html', {
        'course': course,
        'available_students': available_students
    })

@login_required
def bulk_attendance_view(request):
    courses = Course.objects.all()
    selected_course = None
    students = []
    selected_date = datetime.now().strftime('%Y-%m-%d')
    
    if request.method == 'POST':
        course_id = request.POST.get('course')
        selected_date = request.POST.get('date')
        
        if course_id:
            selected_course = get_object_or_404(Course, pk=course_id)
            
            if 'save_attendance' in request.POST:
                student_ids = request.POST.getlist('student_ids')
                
                for s_id in student_ids:
                    status = request.POST.get(f'status_{s_id}', 'Present')
                    Attendance.objects.update_or_create(
                        student_id=s_id,
                        course=selected_course,
                        date=selected_date,
                        defaults={'status': status}
                    )
                return render(request, 'management/attendance_bulk.html', {
                    'courses': courses,
                    'success': f'Attendance for {selected_course.class_name} saved successfully!',
                    'selected_date': selected_date
                })
            else:
                enrollments = selected_course.enrollments.select_related('student').all()
                existing_records = Attendance.objects.filter(
                    course=selected_course, 
                    date=selected_date
                ).values_list('student_id', 'status')
                status_map = {s_id: status for s_id, status in existing_records}
                
                for e in enrollments:
                    students.append({
                        'student': e.student,
                        'status': status_map.get(e.student.id, 'Present')
                    })
                    
    return render(request, 'management/attendance_bulk.html', {
        'courses': courses,
        'selected_course': selected_course,
        'students': students,
        'selected_date': selected_date
    })
