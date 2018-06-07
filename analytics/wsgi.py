import os, sys

sys.path.append('/files/pythonapps/analytics/clt-analytics-dev-py')


from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "analytics.settings.base")

application = get_wsgi_application()
