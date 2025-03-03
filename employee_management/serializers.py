from rest_framework import serializers
from employee_management.models import Employee, Role, Permission, Team, Education, Address

class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = ['id', 'name', 'description']
    
    def create(self, validated_data):
        # Ensure the name is unique (case-insensitive)
        permission_name = validated_data.get("name").strip().lower()
        if Permission.objects.filter(name__iexact=permission_name).exists():
            raise serializers.ValidationError({"name": "A permission with this name already exists."})
        
        return super().create(validated_data)
    


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ['id', 'name', 'description']
        
    def create(self, validated_data):
        team_name = validated_data.get("name").strip().lower()
        if Team.objects.filter(name__iexact=team_name).exists():
            raise serializers.ValidationError({"name": "A team with this name already exists."})
        
        return super().create(validated_data)
    

class RoleSerializer(serializers.ModelSerializer):   
    class Meta:
        model = Role
        fields = ['id', 'title', 'description', 'reports_to', 'employment_type', 'permission']
        
    def create(self, validated_data):
        role_title = validated_data.get("title").strip().lower()
        if Role.objects.filter(title__iexact=role_title).exists():
            raise serializers.ValidationError({"title": "A role with this name already exists."})
        return super().create(validated_data)


class EmployeeSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(read_only=True)
    role = serializers.PrimaryKeyRelatedField(queryset=Role.objects.all())  # Accept role ID
    team = serializers.PrimaryKeyRelatedField(queryset=Team.objects.all(), many=True)  # Accept team IDs
    
    class Meta:
        model = Employee
        fields = ['id', 'user_id', 'phone', 'join_date', 'email', 'birth_date', 'gender', 'social_handle', 'employment_status', 'role', 'team', 'access_level']
    
    
    
class EducationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Education
        fields = ["id", "institution", "course_of_study", "start_date", "end_date"]
        
    def create(self, validated_data):
        employee_id = self.context['employee_id']
        return Education.objects.create(employee_id=employee_id, **validated_data)

class AddressSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Address
        fields = ["employee_id", "country", "city"]
        
    
    def create(self, validated_data):
        employee_id = self.context['employee_id']
        return Address.objects.create(employee_id=employee_id, **validated_data)

