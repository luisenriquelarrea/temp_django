from django.apps import AppConfig


class NominaConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'nomina'
    verbose_name = "nómina"

    def ready(self):
        import nomina.signals