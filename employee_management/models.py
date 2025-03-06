import uuid
from django.db import models
from django.contrib import admin
from django.conf import settings

# Create your models here.
class Team(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    
    # Change the string representation
    def __str__(self) -> str:
        return self.name
    
    # Sort the Team object
    class Meta:
        ordering = ['name']
    
    
class Permission(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    
    # Change the string representation
    def __str__(self) -> str:
        return self.name
    
    # Sort the Permission object
    class Meta:
        ordering = ['name']

class Role(models.Model):
    
    EMPLOYEMENT_TYPE = [
        ('Full-time', 'Full-time'),
        ('Part-time', 'Part-time'),
        ('Contract', 'Contract'),
        ('Associate', 'Associate'),
    ]
        
     
    title = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    reports_to = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL, related_name='surbodinates')
    employment_type = models.CharField(max_length=20, choices=EMPLOYEMENT_TYPE, default="Full-time")
    team = models.ManyToManyField(Team, blank=True)
    permission = models.ManyToManyField(Permission, blank=True)
    
    # Change the string representation
    def __str__(self) -> str:
        return f"{self.title} ({self.employment_type})"
    
    # Sort the Role object
    class Meta:
        ordering = ['title']
    

class Employee(models.Model):
    EMPLOYMENT_STATUS_ACTIVE = "Active"
    EMPLOYMENT_STATUS_INACTIVE = "Inactive"
    
    EMPLOYMENT_STATUS_CHOICES = [
        (EMPLOYMENT_STATUS_ACTIVE, 'Active'),
        (EMPLOYMENT_STATUS_INACTIVE, 'Inactive')
    ]
    
    GENDER_STATUS_CHOICES = [
        ("M", "Male"),
        ("F", "Female")
    ]
    
    
    ACCESS_LEVEL_CHOICES = [
        ("Admin", "Admin"),
        ('Manager', 'Manager'),
        ('Employee', 'Employee'),
        ('Guest', 'Guest')   
    ]
    
    id = models.CharField(
        primary_key=True,  # Make it the primary key
        max_length=14, 
        unique=True, 
        editable=False
    )
    phone = models.CharField(max_length=12)
    birth_date = models.DateField(null=True, blank=True)
    join_date = models.DateField()
    gender = models.CharField(max_length=1, choices=GENDER_STATUS_CHOICES)
    social_handle = models.CharField(max_length=255, null=True, blank=True)
    employment_status = models.CharField(max_length=50, choices=EMPLOYMENT_STATUS_CHOICES, default=EMPLOYMENT_STATUS_ACTIVE)
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True, blank=True)
    team = models.ManyToManyField(Team, blank=True)
    access_level = models.CharField(max_length=100, choices=ACCESS_LEVEL_CHOICES, default="Employee")
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    
    
    def __str__(self) -> str:
        full_name = f"{self.user.first_name} {self.user.last_name}"
        return full_name
    
    def __str__(self):
        return f"{self.user.username} - {self.role.title} ({self.access_level})"
    
    @admin.display(ordering='user__first_name')
    def first_name(self):
        return self.user.first_name
    
    @admin.display(ordering='user__last_name')
    def last_name(self):
        return self.user.last_name
    
    def email(self):
        return self.user.email
    
    class Meta:
        ordering = ['user__first_name', 'user__last_name']

    
    def save(self, *args, **kwargs):
        if not self.id:  # Generate ID only if it doesn't exist
            self.id = {uuid.uuid4().hex[:13].upper()}  # 13 random chars after #
        super().save(*args, **kwargs)
    
    

class Education(models.Model):
    institution = models.CharField(max_length=255)
    course_of_study = models.CharField(max_length=255, null=True, blank=True)
    start_date = models.DateField()
    end_date = models.DateField()
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name="educations")

class Address(models.Model):
    country = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    employee = models.OneToOneField(Employee, on_delete=models.CASCADE, primary_key=True, related_name="address")
    
    def __str__(self):
        return f"{self.employee}'s address"