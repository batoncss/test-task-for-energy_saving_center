import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'for_energy_saving_center.settings')

application = get_wsgi_application()
