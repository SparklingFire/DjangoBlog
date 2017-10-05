from django.apps import AppConfig


class HitConfig(AppConfig):
    name = 'hit'

    def ready(self):
        import hit.signals
