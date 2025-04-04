# Aerten - Employee Management Tool (Backend API)

## Overview

Aerten is a web-based employee management tool designed for businesses of all sizes. This repository contains the backend API for the Role and Permission Management feature, developed as a capstone project for the ALX Backend Engineering program.

## Key Features

- **Permission Management**: Admins can define granular permissions for each role
- **Employee Role Assignment**: Assign and manage employee access levels
- **Role Management**: CRUD operations for organizational roles
- **Custom Role Creation**: Create tailored roles with specific permissions

## Technology Stack

- **Framework**: Django 4.2 + Django REST Framework
- **Database**: MYSQL
- **Testing**: Django Test Framework + Locust for performance testing
- **Authentication**: Djoser JWT (JSON Web Tokens)
<!-- - **Deployment**: Docker-ready configuration -->

## API Endpoints

### Authentication

`POST /api/auth/register/` - User registration  
`POST /api/auth/jwt/create` - Obtain JWT tokens  
`POST /api/auth/refresh/` - Refresh access token

### Roles Management

`GET /api/v1/roles/` - List all roles  
`POST /api/v1/roles/` - Create new role  
`GET /api/v1/roles/{id}/` - Retrieve role details  
`PUT /api/v1/roles/{id}/` - Update role  
`DELETE /api/v1/roles/{id}/` - Delete role

### Permissions

`GET /api/v1/permissions/` - List available permissions  
`POST /api/roles/{id}/permissions/` - Assign permissions to role  
`DELETE /api/roles/{id}/permissions/{perm_id}/` - Remove permission from role

### Employees

`GET /api/v1/employees/` - List all roles  
`POST /api/v1/employees/me` - Get employee profile if available or create by default if not  
`PUT /api/v1/employees/me/` - Update employee profile

### Assign Role To Employee

`POST /api/v1/employees/assign_role/

## Installation

### Prerequisites

- Python 3.12
- MYSQL
- pip

### Setup

```bash
git clone https://github.com/IveeDev/aerten-backend.git
cd aerten-backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## 🧪 Testing

### Unit & Integration Tests

```bash
# Run all tests
python manage.py test

# Run specific test module
python manage.py test apps.roles.tests

# Run with verbose output
python manage.py test --verbosity=2
```

# Install locust

pip install locust

# Run tests (web interface)

locust -f locustfile.py

# Run in command-line mode

locust -f locustfile.py --headless -u 100 -r 10 -t 5m
