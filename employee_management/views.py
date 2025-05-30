from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.core.cache import cache
from rest_framework.response import Response
from rest_framework import status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import serializers
from rest_framework.exceptions import PermissionDenied
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.mixins import CreateModelMixin, ListModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.decorators import action
from .models import Permission, Team, Role, Employee, EmployeeImage, Education, Address, Request
from .serializers import PermissionSerializer, AssignRoleSerializer, TeamSerializer, RoleSerializer, EmployeeSerializer, EmployeeImageSerializer, EducationSerializer, AddressSerializer, RequestSerializer, AddToTeamSerializer
from .filters import RoleFilter, EmployeeFilter, RequestFilter
from .pagination import DefaultPagination
from .permissions import IsAdminOrReadOnly, IsAdminOrManager, IsAdminManagerOrOwner



class BaseViewSet(ModelViewSet):  # Common base ViewSet
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]


# Create your views here.

class PermissionViewSet(BaseViewSet):
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer
    permission_classes = [IsAdminOrReadOnly]
    


class TeamViewSet(BaseViewSet):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    search_fields = ["name"]
    permission_classes = [IsAuthenticated]
    
class RoleViewSet(BaseViewSet):
    queryset = Role.objects.prefetch_related("permission").all()
    serializer_class = RoleSerializer
    filterset_class = RoleFilter
    search_fields = ["title", "description"]
    permission_classes = [IsAdminOrReadOnly]
    
    
class EmployeeFilter(DjangoFilterBackend):
    pass
    
    
    
    
    
class EmployeeViewSet(BaseViewSet):
    queryset = Employee.objects.prefetch_related('team').select_related('role').all()
    serializer_class = EmployeeSerializer
    permission_classes = [IsAdminUser]
    filterset_class = EmployeeFilter
    pagination_class = DefaultPagination
    search_fields = ["user__first_name", "user__last_name"]
    ordering_fields = ["user__first_name"]

    
    
    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsAuthenticated()]
        return [IsAdminOrReadOnly()]
    
    
    @action(detail=False, methods=['GET', 'PUT'], permission_classes=[IsAuthenticated])
    def me(self, request):
        (employee, created) = Employee.objects.get_or_create(user_id=request.user.id)
            
        if request.method == 'GET':
            serializer = EmployeeSerializer(employee)
            response_data = serializer.data
            if not employee.role or not employee.team.exists():
                response_data["message"] = "Your profile is incomplete. Please contact the admin to assign a role and team."
            return Response(response_data)
        elif request.method == 'PUT':
            serializer = EmployeeSerializer(employee, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
    
    @action(detail=False, methods=['post'], url_path='assign_role', serializer_class=AssignRoleSerializer, permission_classes=[IsAdminUser])
    def assign_role(self, request, pk=None):
        serializer = AssignRoleSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        role = serializer.validated_data["role_id"]

        if "employee_id" in serializer.validated_data:
            employee = serializer.validated_data["employee_id"]
            employee.role = role
            employee.save()
            return Response({"message": f"Role assigned to employee {employee.user.username} {employee.id}"}, status=status.HTTP_200_OK)

        if "employee_ids" in serializer.validated_data:
            employees = serializer.validated_data["employee_ids"]
            for employee in employees:
                employee.role = role
                employee.save()
            return Response({"message": f"Role assigned to {len(employees)} employees"}, status=status.HTTP_200_OK)
        
        
    @action(detail=False, methods=['post'], url_path='add_to_team', serializer_class=AddToTeamSerializer, permission_classes=[IsAdminUser])
    def add_to_team(self, request, pk=None):
        serializer = AddToTeamSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        team = serializer.validated_data["team_id"]

        if "employee_id" in serializer.validated_data:
            employee = serializer.validated_data["employee_id"]
            employee.team.add(team)
            return Response({"message": f"Team assigned to employee, {employee.user.username} {employee.id}"}, status=status.HTTP_200_OK)

        if "employee_ids" in serializer.validated_data:
            employees = serializer.validated_data["employee_ids"]
            
            for employee in employees:
                employee.team.add(team)
            return Response({"message": f"Added to {len(employees)} employees"})

class EmployeeImageViewSet(ModelViewSet):
    serializer_class = EmployeeImageSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        
        employee = user.employee
        
        return EmployeeImage.objects.filter(employee=employee)
    
    def get_object(self):
        # Override get_object to return the EmployeeImage for the logged-in user
        return self.get_queryset().first()

class RequestViewSet(BaseViewSet):
    serializer_class = RequestSerializer
    permission_classes = [IsAuthenticated, IsAdminManagerOrOwner]
    filterset_class = RequestFilter
    
    def get_queryset(self):
        user = self.request.user
        if not user:
            return Request.objects.none()
        
        (employee, created) = Employee.objects.get_or_create(user_id=user.id)
        if user.is_staff or employee.access_level in ["Admin", "Manager"]:
            return Request.objects.all()     
        return Request.objects.filter(employee__user=user)
    
    
    
    def get_serializer_context(self):
        # Pass the request object to the serializer context
        context = super().get_serializer_context()
        context['request'] = self.request
        return context
    

    
    def destroy(self, request, *args, **kwargs):
        request_obj = self.get_object()
        
        if request_obj.status in ["Approved", "Reject"]:
            return Response(
                {"detail": "Cannot delete a request that is approved or rejected."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Perform the deletion
        request_obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    @action(detail=True, methods=['PATCH'], permission_classes=[IsAdminOrManager])
    def approve(self, request, pk=None):
        return self._update_request_status(request, pk, "Approved")
    
    @action(detail=True, methods=['PATCH'], permission_classes=[IsAdminOrManager])
    def reject(self, request, pk=None):
        return self._update_request_status(request, pk, "Rejected")
    
    def _update_request_status(self, request, pk, new_status):
        request_obj = self.get_object()
        
        if request_obj.status == new_status:
            return Response(
                {"detail": f"This request is already {new_status}."}, status=status.HTTP_400_BAD_REQUEST
            )
        
        request_obj.status = new_status
        request_obj.approver = request.user
        request_obj.save()
        
        # Return the updated request
        serializer = self.get_serializer(request_obj)  # Pass only the instance
        return Response(serializer.data, status=status.HTTP_200_OK)

    
    def perform_create(self, serializer):
        serializer.save(employee=self.request.user.employee)        
     
    
        
class EducationViewSet(BaseViewSet):
    serializer_class = EducationSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        employee_id = self.kwargs.get('employee_pk')
        if not employee_id:
            return Education.objects.none()  # Prevent errors if employee_pk is missing
        return Education.objects.filter(employee_id=employee_id)
    
    def get_serializer_context(self):
        return {'employee_id': self.kwargs['employee_pk']}
    
    def get_permissions(self):
        if self.request.method in ['POST', 'PUT', 'DELETE']:
            return [IsAdminOrReadOnly()]
        return super().get_permissions()  # Default to IsAuthenticated

class AddressViewSet(BaseViewSet):
    serializer_class = AddressSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        employee_id = self.kwargs.get('employee_pk')
        if not employee_id:
            return Address.objects.none()
        return Address.objects.filter(employee_id=employee_id)
    
    def get_serializer_context(self):
        return {'employee_id': self.kwargs['employee_pk']}
    
    def get_permissions(self):
        if self.request.method in ['POST', 'PUT', 'DELETE']:
            return [IsAdminOrReadOnly()]
        return super().get_permissions()