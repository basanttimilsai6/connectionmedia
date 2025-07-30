from django.urls import path,include
from rest_framework.routers import DefaultRouter
from apps.users.views import UserRegistrationViewSet,UserLogin

router = DefaultRouter()
router.register('register', UserRegistrationViewSet, basename='user-register')


urlpatterns = [
    path('', include(router.urls)),
    path('login/',UserLogin.as_view(),name='login')
]
