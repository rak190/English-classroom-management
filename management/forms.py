from django import forms
from django.contrib.auth.models import User
from .models import Student, Course, Enrollment, Attendance, Homework, HomeworkSubmission, Score, Material, InviteCode

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

class TeacherRegistrationForm(forms.ModelForm):
    invite_code = forms.CharField(max_length=20, required=True, help_text="Enter the secret invite code")
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirm = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']

    def clean_invite_code(self):
        code = self.cleaned_data.get('invite_code')
        if not InviteCode.objects.filter(code=code, is_active=True).exists():
            raise forms.ValidationError("Invalid or inactive invite code.")
        return code

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if password and password_confirm and password != password_confirm:
            self.add_error('password_confirm', "Passwords do not match.")
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user
