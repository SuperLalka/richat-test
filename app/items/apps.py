import os

from django.apps import AppConfig


class ItemsConfig(AppConfig):
    name = 'app.items'

    def ready(self):
        if os.getenv('RUN_CUSTOM_THREADS'):
            from app.items.threads import run_synchronizer

            run_synchronizer()
