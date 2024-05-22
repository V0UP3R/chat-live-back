from django.apps import AppConfig

class SeuAppConfig(AppConfig):
    name = 'user'

    def ready(self):
        import user.signals