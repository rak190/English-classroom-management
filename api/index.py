import os
import sys

# Add the project directory to the sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Set the Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecms_project.settings')

# Import the Django WSGI application
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

# Vercel requires the variable to be named 'app'
app = application
