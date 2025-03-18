from django.contrib.auth.models import User
from rest_framework import status
import pytest

@pytest.fixture
def create_permission(api_client):
    def do_create_permission(permission):
        return api_client.post("/api/v1/permissions/", permission)
    return do_create_permission
    

@pytest.mark.django_db
class TestCreatePermission:
    # @pytest.mark.skip
    def test_if_user_is_anonymous_returns_401(self, create_permission):
        response = create_permission({"name": "a", "description": "aaaaaaa"})
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        
    
    def test_if_user_is_not_admin_returns_403(self, authenticate, create_permission):
        # Act
        authenticate(is_staff=False)
        response = create_permission({"name": "a", "description": "aaaaaaa"})
        # Assert
        assert response.status_code == status.HTTP_403_FORBIDDEN
        
    # User is authenticated and is admin but data is invalid
    def test_if_data_is_invalid_returns_400(self, authenticate, create_permission):
        # Act
        authenticate(is_staff=True)
        response = create_permission({"name": "", "description": "aaaaaaa"})
        # Assert
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data["name"] is not None
        
    def test_if_data_is_valid_returns_201(self, authenticate, create_permission):
        # Act
        authenticate(is_staff=True)
        response = create_permission( {"name": "a", "description": "aaaaaaa"})
        # Assert
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data.get("id") > 0