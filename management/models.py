from django.db import models
from django.contrib.auth.models import User

class Student(models.Model):
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='students')
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other')
    ]
    student_id = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=200)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    grade = models.CharField(max_length=50)
    phone = models.CharField(max_length=20, blank=True, null=True)
    parent_phone = models.CharField(max_length=20)
    join_date = models.DateField()
    photo = models.ImageField(upload_to='students/', blank=True, null=True)

    def __str__(self):
        return f"{self.student_id} - {self.name}"

class Course(models.Model):
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='courses')
    class_name = models.CharField(max_length=200)

    def __str__(self):
        return self.class_name

class Enrollment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='enrollments')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments')

    class Meta:
        unique_together = ('student', 'course')

    def __str__(self):
        return f"{self.student.name} in {self.course.class_name}"

class Attendance(models.Model):
    STATUS_CHOICES = [
        ('Present', 'Present'),
        ('Absent', 'Absent'),
        ('Late', 'Late')
    ]
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='attendances')
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    date = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)

    class Meta:
        unique_together = ('student', 'course', 'date')

    def __str__(self):
        return f"{self.student.name} - {self.date} - {self.status}"

class Homework(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='homeworks')
    title = models.CharField(max_length=200)
    deadline = models.DateField()

    def __str__(self):
        return f"{self.title} ({self.course.class_name})"

class HomeworkSubmission(models.Model):
    STATUS_CHOICES = [
        ('Submitted', 'Submitted'),
        ('Not Submitted', 'Not Submitted'),
        ('Late Submission', 'Late Submission')
    ]
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='homework_submissions')
    homework = models.ForeignKey(Homework, on_delete=models.CASCADE, related_name='submissions')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Not Submitted')

    class Meta:
        unique_together = ('student', 'homework')

    def __str__(self):
        return f"{self.student.name} - {self.homework.title} - {self.status}"

class Score(models.Model):
    TYPE_CHOICES = [
        ('Quiz', 'Quiz'),
        ('Homework', 'Homework'),
        ('Speaking', 'Speaking'),
        ('Midterm', 'Midterm'),
        ('Final', 'Final')
    ]
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='scores')
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    score_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    value = models.FloatField()
    date = models.DateField(auto_now_add=True, null=True)

    def __str__(self):
        return f"{self.student.name} - {self.score_type}: {self.value}"

class Material(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='materials')
    title = models.CharField(max_length=200)
    file = models.FileField(upload_to='materials/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Schedule(models.Model):
    DAY_CHOICES = [
        ('MON', 'Monday'),
        ('TUE', 'Tuesday'),
        ('WED', 'Wednesday'),
        ('THU', 'Thursday'),
        ('FRI', 'Friday'),
        ('SAT', 'Saturday'),
        ('SUN', 'Sunday'),
    ]
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='schedules')
    day = models.CharField(max_length=3, choices=DAY_CHOICES)
    start_time = models.TimeField()
    end_time = models.TimeField()

    class Meta:
        ordering = ['day', 'start_time']

    def __str__(self):
        return f"{self.course.class_name} - {self.get_day_display()} ({self.start_time.strftime('%H:%M')} - {self.end_time.strftime('%H:%M')})"

class Notice(models.Model):
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='notices')
    title = models.CharField(max_length=200)
    content = models.TextField()
    author_name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    icon = models.CharField(max_length=50, default='bx-book-open', help_text="Boxicons class, e.g. bx-calendar-event")
    
    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

class Event(models.Model):
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='events')
    title = models.CharField(max_length=200)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField(null=True, blank=True)
    audience = models.CharField(max_length=100, help_text="e.g. Grade 7, All Staff")
    
    class Meta:
        ordering = ['date', 'start_time']

    def __str__(self):
        return self.title

class InviteCode(models.Model):
    code = models.CharField(max_length=20, unique=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.code
