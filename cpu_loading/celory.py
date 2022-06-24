# import os
# from celery import Celery
#
# # для прописания настроек для Celery
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cpu_loading.settings')
#
# app = Celery('cpu_loading')
# app.config_from_object('django.conf:settings', namespace='CELERY')  # для зацепки настроек по имени CELERY
# app.autodiscover_tasks()  # автоматически подкреплять таски