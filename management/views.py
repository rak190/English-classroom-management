from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.core.management import call_command
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.db.utils import OperationalError
import traceback
import csv
from datetime import datetime, timedelta
from django.db.models import Count, Avg
from django.utils import timezone
from .models import Student, Course, Enrollment, Attendance, Homework, HomeworkSubmission, Score, Material, Notice, Event, InviteCode
from .forms import StudentForm, CourseForm, AttendanceForm, MaterialForm, TeacherRegistrationForm

def register_teacher(request):
    if request.method == 'POST':
        form = TeacherRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('management:dashboard')
    else:
        form = TeacherRegistrationForm()
    return render(request, 'management/register.html', {'form': form})

@login_required
def dashboard(request):
    import json
    today = timezone.now().date()
    
    total_students = Student.objects.filter(teacher=request.user).count()
    active_classes = Course.objects.filter(teacher=request.user).count()
    
    today_attendance_present = Attendance.objects.filter(course__teacher=request.user, date=today, status='Present').count()
    today_attendance_total = Attendance.objects.filter(course__teacher=request.user, date=today).count()
    
    hw_submitted = HomeworkSubmission.objects.filter(student__teacher=request.user, status='Submitted').count()
    hw_total = HomeworkSubmission.objects.filter(student__teacher=request.user).count()

    # Chart 1: Gender distribution
    male_count = Student.objects.filter(teacher=request.user, gender='M').count()
    female_count = Student.objects.filter(teacher=request.user, gender='F').count()
    gender_data = [male_count, female_count]

    # Chart 2: Attendance over last 5 days
    attendance_labels = []
    attendance_data = []
    for i in range(4, -1, -1):
        d = today - timedelta(days=i)
        attendance_labels.append(d.strftime('%a'))
        present = Attendance.objects.filter(course__teacher=request.user, date=d, status='Present').count()
        total = Attendance.objects.filter(course__teacher=request.user, date=d).count()
        pct = (present / total * 100) if total > 0 else 0
        attendance_data.append(round(pct))

    # Chart 3: Progress tracking (Scores per course)
    course_averages = Score.objects.filter(student__teacher=request.user).values('course__class_name').annotate(average=Avg('value'))[:8]
    if course_averages:
        progress_labels = [c['course__class_name'] for c in course_averages]
        progress_data = [round(c['average'], 1) for c in course_averages]
    else:
        progress_labels = ["No Data"]
        progress_data = [0]

    # Notices & Events
    recent_notices = Notice.objects.filter(teacher=request.user).order_by('-created_at')[:3]
    upcoming_events = Event.objects.filter(teacher=request.user, date__gte=today).order_by('date', 'start_time')[:3]

    context = {
        'total_students': total_students,
        'active_classes': active_classes,
        'today_attendance_present': today_attendance_present,
        'today_attendance_total': today_attendance_total,
        'hw_submitted': hw_submitted,
        'hw_total': hw_total,
        'gender_data': json.dumps(gender_data),
        'attendance_labels': json.dumps(attendance_labels),
        'attendance_data': json.dumps(attendance_data),
        'progress_labels': json.dumps(progress_labels),
        'progress_data': json.dumps(progress_data),
        'recent_notices': recent_notices,
        'upcoming_events': upcoming_events,
    }
    return render(request, 'management/dashboard.html', context)

@login_required
def student_list(request):
    students = Student.objects.filter(teacher=request.user).order_by('-join_date')
    return render(request, 'management/student_list.html', {'students': students})

@login_required
def student_create(request):
    if request.method == 'POST':
        form = StudentForm(request.POST, request.FILES)
        if form.is_valid():
            student = form.save(commit=False)
            student.teacher = request.user
            student.save()
            return redirect('management:student_list')
    else:
        form = StudentForm()
    return render(request, 'management/student_form.html', {'form': form, 'is_edit': False})

@login_required
def student_edit(request, student_id):
    student = get_object_or_404(Student, pk=student_id, teacher=request.user)
    if request.method == 'POST':
        form = StudentForm(request.POST, request.FILES, instance=student)
        if form.is_valid():
            form.save()
            return redirect('management:student_list')
    else:
        form = StudentForm(instance=student)
    return render(request, 'management/student_form.html', {'form': form, 'is_edit': True})

@login_required
def student_delete(request, student_id):
    student = get_object_or_404(Student, pk=student_id, teacher=request.user)
    if request.method == 'POST':
        student.delete()
        return redirect('management:student_list')
    return render(request, 'management/confirm_delete.html', {'object': student, 'title': 'Delete Student'})

@login_required
def class_list(request):
    courses = Course.objects.filter(teacher=request.user).annotate(student_count=Count('enrollments')).all()
    return render(request, 'management/class_list.html', {'courses': courses})

@login_required
def class_create(request):
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            course = form.save(commit=False)
            course.teacher = request.user
            course.save()
            return redirect('management:class_list')
    else:
        form = CourseForm()
    return render(request, 'management/class_form.html', {'form': form, 'is_edit': False})

@login_required
def class_edit(request, course_id):
    course = get_object_or_404(Course, pk=course_id, teacher=request.user)
    if request.method == 'POST':
        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            return redirect('management:class_list')
    else:
        form = CourseForm(instance=course)
    return render(request, 'management/class_form.html', {'form': form, 'is_edit': True})

@login_required
def class_delete(request, course_id):
    course = get_object_or_404(Course, pk=course_id, teacher=request.user)
    if request.method == 'POST':
        course.delete()
        return redirect('management:class_list')
    return render(request, 'management/confirm_delete.html', {'object': course, 'title': 'Delete Class'})

@login_required
def class_detail(request, course_id):
    course = get_object_or_404(Course, pk=course_id, teacher=request.user)
    enrollments = course.enrollments.select_related('student').all()
    return render(request, 'management/class_detail.html', {'course': course, 'enrollments': enrollments})

@login_required
def remove_student_from_class(request, course_id, student_id):
    course = get_object_or_404(Course, pk=course_id, teacher=request.user)
    if request.method == 'POST':
        enrollment = get_object_or_404(Enrollment, course=course, student_id=student_id)
        enrollment.delete()
    return redirect('management:class_detail', course_id=course.id)

@login_required
def attendance_view(request):
    if request.method == 'POST':
        form = AttendanceForm(request.POST)
        if form.is_valid():
            # Validate course belongs to teacher
            if form.cleaned_data['course'].teacher == request.user:
                form.save()
            return redirect('management:attendance_view')
    else:
        form = AttendanceForm()
        form.fields['course'].queryset = Course.objects.filter(teacher=request.user)
        form.fields['student'].queryset = Student.objects.filter(teacher=request.user)
        
    attendances = Attendance.objects.filter(course__teacher=request.user).order_by('-date')
    return render(request, 'management/attendance.html', {'form': form, 'attendances': attendances})

@login_required
def homework_view(request):
    submissions = HomeworkSubmission.objects.filter(student__teacher=request.user).select_related('student', 'homework')
    return render(request, 'management/homework.html', {'submissions': submissions})

@login_required
def homework_status_edit(request, submission_id):
    submission = get_object_or_404(HomeworkSubmission, pk=submission_id, student__teacher=request.user)
    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in dict(HomeworkSubmission.STATUS_CHOICES):
            submission.status = new_status
            submission.save()
    return redirect('management:homework_view')

@login_required
def score_view(request):
    scores = Score.objects.filter(student__teacher=request.user).select_related('student', 'course')
    
    # Calculate average scores
    student_averages = Score.objects.filter(student__teacher=request.user).values('student__name').annotate(average=Avg('value'))
    
    return render(request, 'management/scores.html', {
        'scores': scores,
        'student_averages': student_averages
    })

@login_required
def material_view(request):
    if request.method == 'POST':
        form = MaterialForm(request.POST, request.FILES)
        if form.is_valid():
            if form.cleaned_data['course'].teacher == request.user:
                form.save()
            return redirect('management:material_view')
    else:
        form = MaterialForm()
        form.fields['course'].queryset = Course.objects.filter(teacher=request.user)
        
    materials = Material.objects.filter(course__teacher=request.user).order_by('-uploaded_at')
    return render(request, 'management/materials.html', {'form': form, 'materials': materials})

@login_required
def schedule_view(request):
    from .models import Schedule
    schedules = Schedule.objects.filter(course__teacher=request.user).select_related('course').order_by('day', 'start_time')
    
    # Group schedules by day for easier rendering in template
    days = ['MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT', 'SUN']
    schedule_by_day = {day: [] for day in days}
    for s in schedules:
        schedule_by_day[s.day].append(s)
        
    return render(request, 'management/schedule.html', {'schedule_by_day': schedule_by_day})

@login_required
def progress_tracking_view(request):
    # This view will gather overall data for charts
    courses = Course.objects.filter(teacher=request.user)
    # Simple aggregation: Average score per course
    course_averages = Score.objects.filter(course__teacher=request.user).values('course__class_name').annotate(average=Avg('value'))
    
    return render(request, 'management/progress.html', {
        'courses': courses,
        'course_averages': list(course_averages)
    })

@login_required
def parent_report_view(request, student_id):
    student = get_object_or_404(Student, pk=student_id, teacher=request.user)
    
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
        import urllib.request
        file_data = None
        
        # Check if Google Sheet URL is provided
        sheet_url = request.POST.get('google_sheet_url', '').strip()
        if sheet_url:
            try:
                # Convert Google Sheet URL to CSV export URL
                # Typical URL: https://docs.google.com/spreadsheets/d/SPREADSHEET_ID/edit#gid=0
                if '/edit' in sheet_url:
                    csv_url = sheet_url.split('/edit')[0] + '/export?format=csv'
                else:
                    csv_url = sheet_url
                    
                req = urllib.request.Request(csv_url, headers={'User-Agent': 'Mozilla/5.0'})
                with urllib.request.urlopen(req) as response:
                    file_data = response.read().decode('utf-8-sig').splitlines()
            except Exception as e:
                return render(request, 'management/student_bulk_import.html', {'error': f'Failed to fetch Google Sheet: {str(e)}. Make sure the link is set to "Anyone with the link can view".'})
        
        # Fallback to CSV upload
        elif 'csv_file' in request.FILES and request.FILES['csv_file']:
            csv_file = request.FILES['csv_file']
            if not csv_file.name.endswith('.csv'):
                return render(request, 'management/student_bulk_import.html', {'error': 'Please upload a valid CSV file.'})
            file_data = csv_file.read().decode('utf-8-sig').splitlines()
            
        else:
            return render(request, 'management/student_bulk_import.html', {'error': 'Please provide either a CSV file or a Google Sheet URL.'})
            
        try:
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
                    join_date=join_date,
                    teacher=request.user
                ))
            
            if students_to_create:
                Student.objects.bulk_create(students_to_create)
                return render(request, 'management/student_bulk_import.html', {'success': f'Successfully imported {len(students_to_create)} students!'})
            else:
                return render(request, 'management/student_bulk_import.html', {'error': 'No new students imported. Make sure student_ids are unique and required columns are present.'})
                
        except Exception as e:
            return render(request, 'management/student_bulk_import.html', {'error': f'Error processing file: {str(e)}'})
            
    if 'download_template' in request.GET:
        response = HttpResponse(content_type='text/csv; charset=utf-8-sig')
        response['Content-Disposition'] = 'attachment; filename="student_import_template.csv"'
        # Write BOM to ensure Excel opens it as UTF-8
        response.write('\ufeff')
        writer = csv.writer(response)
        writer.writerow(['student_id', 'name', 'gender', 'grade', 'parent_phone', 'phone', 'join_date'])
        writer.writerow(['STU-1001', 'សុខ តារា', 'M', 'ថ្នាក់ទី ៨', '012345678', '098765432', '2025-09-01'])
        writer.writerow(['STU-1002', 'មាស បុប្ផា', 'F', 'ថ្នាក់ទី ៨', '012345679', '', '2025-09-01'])
        return response
        
    return render(request, 'management/student_bulk_import.html')

@login_required
def class_bulk_enroll(request, course_id):
    course = get_object_or_404(Course, pk=course_id, teacher=request.user)
    enrolled_student_ids = course.enrollments.values_list('student_id', flat=True)
    available_students = Student.objects.filter(teacher=request.user).exclude(id__in=enrolled_student_ids).order_by('name')
    
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
    courses = Course.objects.filter(teacher=request.user)
    selected_course = None
    students = []
    selected_date = datetime.now().strftime('%Y-%m-%d')
    
    if request.method == 'POST':
        course_id = request.POST.get('course')
        selected_date = request.POST.get('date')
        
        if course_id:
            selected_course = get_object_or_404(Course, pk=course_id, teacher=request.user)
            
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
