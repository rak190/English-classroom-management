import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecms_project.settings')
django.setup()
from django.contrib.auth.models import User
from django.test import Client

c = Client()
c.login(username='testadmin', password='password')

resp = c.post('/students/add/', {'student_id': 'STU-999', 'name': 'Test', 'grade': 'Grade 10', 'gender': 'M', 'parent_phone': '123456789'})
print('Status:', resp.status_code)
content = resp.content.decode('utf-8')
if resp.context and 'form' in resp.context:
    print('Form errors:', resp.context['form'].errors)
