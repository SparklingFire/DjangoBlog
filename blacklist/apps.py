from django.apps import AppConfig


class BlacklistConfig(AppConfig):
    name = 'blacklist'

    def ready(self):
        import blacklist.signals
