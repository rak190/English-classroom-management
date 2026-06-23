from django.contrib import admin
from .models import Student, Course, Enrollment, Attendance, Homework, HomeworkSubmission, Score, Material, Schedule

admin.site.register(Student)
admin.site.register(Course)
admin.site.register(Enrollment)
admin.site.register(Attendance)
admin.site.register(Homework)
admin.site.register(HomeworkSubmission)
admin.site.register(Score)
admin.site.register(Material)
admin.site.register(Schedule)
