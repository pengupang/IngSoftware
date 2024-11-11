from django.apps import AppConfig


class AppsoftConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'AppSoft'



class TuAppConfig(AppConfig):
    name = 'AppSoft'

    def ready(self):
        import AppSoft.signals 
