from django.shortcuts import render
from .models import Employee,Department,Project,User,UserDetails
from .serializers import EmployeeSerializer,DepartmentSerializer,ProjectSerializer,UserDetailsSerializer,UserSerializer,SignupSerializer,LoginSerializer
from rest_framework import filters
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework_simplejwt.tokens import RefreshToken
#from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework import status
from rest_framework.response import Response
from django.contrib.auth import authenticate
# Create your views here.
#EmployeeViewSet-->class name
#viewsets.ModelViewSet-->DRF class that provides implementations for CRUD operations
class EmployeeViewSet(viewsets.ModelViewSet):
    permission_classes=[IsAuthenticated]
    queryset=Employee.objects.all() #queryset is the collection of objects from the database using ORM
    serializer_class=EmployeeSerializer #serializer denotes which serializer we used
    filter_backends=[filters.SearchFilter] #search filter is used to filter the data based on the search query
        #use the search filter functionality andthe SearchFilter is a builtin feature provided by Django
    #specifies the fields in which the search should be performed
    search_fields=["EmployeeName","Designation"]
class DepartmentViewSet(viewsets.ModelViewSet):
    queryset=Department.objects.all()
    serializer_class=DepartmentSerializer
class ProjectViewSet(viewsets.ModelViewSet):
    queryset=Project.objects.all()
    serializer_class=ProjectSerializer
class UserViewSet(viewsets.ModelViewSet):
    queryset=User.objects.all()
    serializer_class=UserSerializer
class UserDetailsViewSet(viewsets.ModelViewSet):
    queryset=UserDetails.objects.all()
    serializer_class=UserDetailsSerializer
    #class based api THAT MEANS APIVIEW IS PROVIDED BY DJANGO RESTFRAMEWORK
class SignupAPIView(APIView):
    permission_classes=[AllowAny]
    def post(self,request):
        serializer=SignupSerializer(data=request.data)#serializer validates the incoming data
        if serializer.is_valid():
            #if the validation success it will create the new user
            #drf internally calls create method inside the serializer
            user=serializer.save()
            #if token already exists return the existing token otherwise it creates the new one
            # token,created=Token.objects.get_or_create(user=user)
            refresh=RefreshToken.for_user(user)
            return Response({
                "user_id":user.id,
                "user_name":user.username,
                "access":str(refresh.access_token),
                "refresh":str(refresh),
                # "token":token.key,
                "role":user.groups.all()[0].id if user.groups.exists() else None
                
            },status=status.HTTP_201_CREATED)
        #if there is any validation error then else block will execute
        else:
            res={'status':status.HTTP_400_BAD_REQUEST,'data':serializer.errors}
            return Response(res,status=status.HTTP_400_BAD_REQUEST)
        
class LoginAPIView(APIView):
    permission_classes=[AllowAny]
    #runs when post/login is called
    def post(self,request):
        #creates a serializer obj and it receives username and password
        serializer=LoginSerializer(data=request.data)
        #serializer will validate the data
        if serializer.is_valid():
            username=serializer.validated_data["username"]
            password=serializer.validated_data["password"]
            user=authenticate(request,username=username,password=password)
            if user is not None:
                refresh=RefreshToken.for_user(user)
                # token=Token.objects.get(user=user)
                response={
                    "status":status.HTTP_200_OK,
                    "message":"success",
                    "username":user.username,
                    "access":str(refresh.access_token),
                    "refresh":str(refresh),
                    # "token":token.key,
                    "role":user.groups.all()[0].id if user.groups.exists() else None
                }
                return Response(response,status=status.HTTP_200_OK)
            else:
                response={
                    "status":status.HTTP_401_UNAUTHORIZED,
                    "message":"Invalid email or password"
                }
                return Response(response,status=status.HTTP_401_UNAUTHORIZED)
        response={
            "status":status.HTTP_400_BAD_REQUEST,
            "message":"BAD REQUEST",
            "data":serializer.errors
           }  
        return Response(response,status=status.HTTP_400_BAD_REQUEST)