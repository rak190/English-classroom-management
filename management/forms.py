from django import forms
from .models import Student, Course, Enrollment, Attendance, Homework, HomeworkSubmission, Score, Material

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['student_id', 'name', 'gender', 'grade', 'phone', 'parent_phone', 'join_date', 'photo']
        widgets = {
            'join_date': forms.DateInput(attrs={'type': 'date'}),
        }

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['class_name']

class AttendanceForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = ['student', 'course', 'date', 'status']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }

class MaterialForm(forms.ModelForm):
    class Meta:
        model = Material
        fields = ['course', 'title', 'file']
