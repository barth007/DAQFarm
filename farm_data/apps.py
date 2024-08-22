from django.apps import AppConfig


class FarmDataConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'farm_data'
    def ready(self):
        import farm_data.signals
