from django.contrib.auth.models import User
from rest_framework import status
from model_bakery import baker
from employee_management.models import Employee, Role, Team
import pytest


# Fixtures for EmployeeViewSet
@pytest.fixture
def create_employee(api_client):
    def do_create_employee(employee):
        return api_client.post("/api/v1/employees/", employee)
    return do_create_employee

@pytest.fixture
def update_employee(api_client):
    def do_update_employee(id, employee):
        return api_client.patch(f'/api/v1/employees/{id}/', employee)
    return do_update_employee

@pytest.fixture
def delete_employee(api_client):
    def do_delete_employee(id):
        return api_client.delete(f'/api/v1/employees/{id}/')
    return do_delete_employee

@pytest.fixture
def retrieve_employee(api_client):
    def do_retrieve_employee(id):
        return api_client.get(f'/api/v1/employees/{id}/')
    return do_retrieve_employee


@pytest.fixture
def get_me(api_client):
    def do_get_me():
        return api_client.get('/api/v1/employees/me/')
    return do_get_me

@pytest.fixture
def update_me(api_client):
    def do_update_me(data):
        return api_client.put('/api/v1/employees/me/', data)
    return do_update_me

@pytest.fixture
def assign_role(api_client):
    def do_assign_role(data):
        return api_client.post('/api/v1/employees/assign_role/', data)
    return do_assign_role