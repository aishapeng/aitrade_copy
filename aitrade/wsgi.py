import os
from django.core.wsgi import get_wsgi_application
from whitenoise import WhiteNoise


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "aitrade.settings")
application = get_wsgi_application()
application = WhiteNoise(application, root='/home/ubuntu/aitrade_copy/static')
# application = WhiteNoise(application, root='/Users/aishapeng/Dev/aitrade/aitrade/static')
