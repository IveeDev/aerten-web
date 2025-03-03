from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework.response import Response
from rest_framework import status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.decorators import action
from .models import Permission, Team, Role, Employee, Education, Address
from .serializers import PermissionSerializer, TeamSerializer, RoleSerializer, EmployeeSerializer, EducationSerializer, AddressSerializer
from .filters import RoleFilter, EmployeeFilter
from .pagination import DefaultPagination
from .permissions import IsAdminOrReadOnly



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
    
    


class EmployeeViewSet(CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, GenericViewSet):
    queryset = Employee.objects.prefetch_related('team').select_related('role').all()
    serializer_class = EmployeeSerializer
    filterset_class = EmployeeFilter
    pagination_class = DefaultPagination
    search_fields = ["user__first_name", "user__last_name"]
    ordering_fields = ["user__first_name"]
    # permission_classes = [IsAuthenticated]
    
    
    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsAdminOrReadOnly()]
    
    @action(detail=False, methods=['GET', 'PUT'], permission_classes=[IsAuthenticated])
    def me(self, request):
        (employee, created) = Employee.objects.get_or_create(user_id=request.user.id, defaults={"join_date": timezone.now()})
        
         # If employee is newly created, make sure it has a role
        if created and employee.role is None:
            default_role = Role.objects.filter(name="Employee").first()
            employee.role = default_role
            employee.save()
            
        if request.method == 'GET':
            serializer = EmployeeSerializer(employee)
            return Response(serializer.data)
        elif request.method == 'PUT':
            serializer = EmployeeSerializer(employee, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
    
    @action(detail=True, methods=['post'], permission_classes=[IsAdminUser])
    def assign_role(self, request, pk=None):
        employee = get_object_or_404(Employee, pk=pk)
        role_id = request.data.get('role_id')

        if not role_id:
            return Response({"error": "Role ID is required"}, status=status.HTTP_400_BAD_REQUEST)

        role = get_object_or_404(Role, pk=role_id)
        employee.role = role
        employee.save()

        return Response({"message": f"Role '{role.name}' assigned to {employee.user.username}"}, status=status.HTTP_200_OK)

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