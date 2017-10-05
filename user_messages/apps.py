from django.apps import AppConfig


class UserMessagesConfig(AppConfig):
    name = 'user_messages'

    def ready(self):
        import user_messages.signals
