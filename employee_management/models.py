from django.db import models

# Create your models here.
class Team(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    
    
class Permission(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=50)

class Role(models.Model):
    ACCESS_LEVEL_CHOICES = [
        ("Admin", "Admin"),
        ('Manager', 'Manager'),
        ('Employee', 'Employee'),
        ('Guest', 'Guest')
        
    ]
    
    
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=255)
    access_level = models.CharField(max_length=50, choices=ACCESS_LEVEL_CHOICES, default="Employee")
    reports_to = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL)
    team = models.ManyToManyField(Team)
    permission = models.ManyToManyField(Permission)
    

class Employee(models.Model):
    EMPLOYMENT_STATUS_ACTIVE = "Active"
    EMPLOYMENT_STATUS_INACTIVE = "Inactive"
    
    EMPLOYMNET_STATUS_CHOICES = [
        (EMPLOYMENT_STATUS_ACTIVE, 'Active'),
        (EMPLOYMENT_STATUS_INACTIVE, 'Inactive')
    ]
    
    GENDER_STATUS_CHOICES = [
        ("M", "Male"),
        ("F", "Female")
    ]
    
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=100)
    join_date = models.DateField()
    gender = models.CharField(max_length=1, choices=GENDER_STATUS_CHOICES)
    social_handle = models.CharField(max_length=100, null=True)
    employment_status = models.CharField(max_length=50, choices=EMPLOYMNET_STATUS_CHOICES, default=EMPLOYMENT_STATUS_ACTIVE)
    role = models.ForeignKey(Role, on_delete=models.PROTECT)
    team = models.ManyToManyField(Team)



    
class Education(models.Model):
    institution = models.CharField(max_length=100)
    year_admitted = models.DateField()
    year_graduated = models.DateField()
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)

class Address(models.Model):
    country = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)