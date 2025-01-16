from django.contrib import admin
from . import models

# Register your models here.
@admin.register(models.Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "description"]
    list_editable = ["name", "description"]
    list_per_page = 10
    
    
    
@admin.register(models.Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ["id", "title", "description", "access_level"]
    list_editable = ["title", "description", "access_level"]
    
@admin.register(models.Permission)
class PermissionAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "description"]
    list_editable = ["name", "description"]
    

@admin.register(models.Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ["id", "first_name", "last_name", "email", "phone", "birth_date", "join_date", "gender", "social_handle", "employment_status", "role", "get_team"]
    list_editable = ["first_name", "last_name", "email", "phone", "birth_date", "join_date", "gender", "social_handle", "employment_status"]
    list_per_page = 10
    list_select_related = ["role"]
    
    
    # Many to Many relationship
    def get_team(self, employee):
        return ", ".join([team.name for team in employee.team.all()])
    get_team.short_description = 'Team'
    
@admin.register(models.Education)
class EducationAdmin(admin.ModelAdmin):
    list_display = ["id", "institution", "course_of_study", "start_date", "end_date", "employee"]
    list_editable = ["institution", "course_of_study"]
    list_select_related = ["employee"]