from django.apps import AppConfig


class UserConfig(AppConfig):
    name = 'users'

    def ready(self):
        import users.signals
