from apps.notifications.views import NotificationViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('notifications', NotificationViewSet, basename='notifications')
urlpatterns = router.urls