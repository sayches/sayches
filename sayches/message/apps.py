from django.apps import AppConfig


class MessagesConfig(AppConfig):
    name = 'message'
    verbose_name = "Messages"

    def ready(self):
        import message.signals