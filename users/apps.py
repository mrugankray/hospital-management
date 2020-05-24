from django.apps import AppConfig


class UsersConfig(AppConfig):
    name = 'users'

    def read(self):
        import users.signals