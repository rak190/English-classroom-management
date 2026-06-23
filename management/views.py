from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
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
