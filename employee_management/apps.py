from django.apps import AppConfig


class EmployeeManagementConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'employee_management'
    
    
    def ready(self) -> None:
        import employee_management.signals.handlers 
