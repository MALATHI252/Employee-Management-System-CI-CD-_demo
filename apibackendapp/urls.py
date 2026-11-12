#default router is a class that automatically creates urls for ViewSets.
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView
from .import views
from django.urls import path
router=DefaultRouter()
router.register(r'employees',views.EmployeeViewSet)
router.register(r'departments',views.DepartmentViewSet)
router.register(r'projects',views.ProjectViewSet)
#SignupAPIView is an APIView,not a Viewset
urlpatterns=[
    path("signup/",views.SignupAPIView.as_view(),name="user-signup"),
    path("login/",views.LoginAPIView.as_view(),name="user-login"),
    path("token/refresh/",TokenRefreshView.as_view(),name="token_refresh"),
    
]
urlpatterns+=router.urls