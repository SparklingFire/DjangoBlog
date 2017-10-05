from django.apps import AppConfig


class TagConfig(AppConfig):
    name = 'tag'

    def ready(self):
        import tag.signals
