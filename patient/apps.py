from django.apps import AppConfig


class PatientConfig(AppConfig):
    name = 'patient'

    def ready(self):
        import patient.signals