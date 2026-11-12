from rest_framework import serializers
from .models import Department,Employee,Project,UserDetails
from datetime import date
import re
from django.contrib.auth.models import User,Group
from django.contrib.auth.hashers import make_password
#validation 1:dateOfJoining current date
#validation 2:employeeName should be characters,no special character
#validation of dateOfJoining
def date_of_joining_restriction(dateOfJoining):
    today=date.today()
    if dateOfJoining!=today:
        raise serializers.ValidationError(" The Date of joining must be today")
    return dateOfJoining
#validation for employeeName
def name_validation(employeeName):
    if len(employeeName)<3 or not re.match("^[A-Za-z]+$",employeeName):
        raise serializers.ValidationError("Name must be atleast 3 letters and contain only alphabetic characters")
    return employeeName
#validation for designation
def designation_validation(designation):
    if len(designation)<3 or not re.match("^[A-Za-z]+$",designation):
        raise serializers.ValidationError("Designation must be at least 3 letters and contain only alphabetic characters")
    return designation
#validation for contact number
def contact_validation(contact):
    if not re.match("^[0-9]{10}$",contact):
        raise serializers.ValidationError("Contact number must be 10 digits")
    return contact
# def department_name_validation(Department):
#     if len(Department)<3 or not re.match("^[A-Za-z]+$",Department):
#         raise serializers.ValidationError("Department name must be at least 3 letters and contain only alphabetic characters")
#     return Department
#department serializer
class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model=Department
        fields='__all__'
#employee serializer
class EmployeeSerializer(serializers.ModelSerializer):
    Department=DepartmentSerializer(source='DepartmentId',read_only=True)
    DateOfJoining=serializers.DateField(validators=[date_of_joining_restriction])
    EmployeeName=serializers.CharField(max_length=200,required=True,validators=[name_validation])
    Contact=serializers.CharField(max_length=10,required=True,validators=[contact_validation])
    Designation=serializers.CharField(max_length=200,required=True,validators=[designation_validation])
    # Department=serializers.CharField(max_length=200,required=True,validators=[department_name_validation])
    #show project details
    project_details=serializers.StringRelatedField(source='projects',many=True,read_only=True)
    class Meta:
        model=Employee
        fields=('EmployeeId','EmployeeName','Designation','DateOfJoining','Contact','IsActive','DepartmentId','Department','project_details')
#project serializer
class ProjectSerializer(serializers.ModelSerializer):
    #employees-->get the data for employee-DETAILS FROM THE EMPLOYEES FIELD OF THE PROJECT MODEL
    employee_details=EmployeeSerializer(source='employees',required=False,many=True,read_only=True)
    #READ_ONLY=TRUE WHY MEANS ONLY FOR VIEWING NOT FOR CREATION OR UPDATION
    class Meta:
        model=Project
        fields=('id','name','employees','employee_details')
class UserDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model=UserDetails
        fields='__all__'
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=('id','username')
    #receives the registration data validates it and hashes the password creates the user and assigns the user to a group and finaaly returns the created user
class SignupSerializer(serializers.ModelSerializer):
    group_name=serializers.CharField(write_only=True,required=False)
    #customizing tge create method
    
    def create(self,validated_data):
        group_name=validated_data.pop("group_name",None)
        #hash the password
        validated_data["password"]=make_password(validated_data.get("password"))
        #create the user
        user=super(SignupSerializer,self).create(validated_data)
        if group_name:
            group,created=Group.objects.get_or_create(name=group_name)
            user.groups.add(group)
        return user
    class Meta:
        model=User
        fields=['username','password','group_name']
class LoginSerializer(serializers.ModelSerializer):
    #field to get username from user
    username=serializers.CharField() 
    #field to get password from user
    password=serializers.CharField(write_only=True)
    class Meta:
        model=User
        fields=['username','password']