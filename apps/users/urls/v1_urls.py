from django.urls import path
from rest_framework.routers import DefaultRouter
from apps.users.views import UserRegistrationViewSet,UserLogin,UserSearchView

router = DefaultRouter()
router.register('register', UserRegistrationViewSet, basename='user-register')

urlpatterns = router.urls

urlpatterns += [
    path('login/',UserLogin.as_view(),name='login'),
    path('search/',UserSearchView.as_view(),name="search")
]
