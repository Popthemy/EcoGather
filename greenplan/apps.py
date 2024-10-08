from django.apps import AppConfig


class GreenplanConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'greenplan'

    def ready(self):
        import greenplan.signals
