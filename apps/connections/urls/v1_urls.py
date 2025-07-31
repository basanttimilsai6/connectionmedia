from rest_framework.routers import DefaultRouter
from apps.connections.views import ConnectionRequestViewSet

router = DefaultRouter()
router.register('connections', ConnectionRequestViewSet, basename='connections')

urlpatterns = router.urls