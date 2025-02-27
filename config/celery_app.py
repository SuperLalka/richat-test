import os

from celery import Celery
from django.apps import AppConfig, apps


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

app = Celery("app")
app.config_from_object("django.conf:settings", namespace="CELERY")


class CeleryAppConfig(AppConfig):
    name = "config.celery_app"
    verbose_name = "Celery Config"

    def ready(self) -> None:
        installed_apps = [app_config.name for app_config in apps.get_app_configs()]
        app.autodiscover_tasks(lambda: installed_apps, force=True)
