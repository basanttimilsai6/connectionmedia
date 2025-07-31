from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from apps.notifications.models import Notification
from apps.notifications.serializers.v1_serializers import NotificationSerializer
from core.response import MyResponse
from rest_framework.throttling import UserRateThrottle
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.parsers import JSONParser
from drf_spectacular.utils import extend_schema
from apps.notifications.services.v1_services import NotificationServices as ns


class NotificationViewSet(viewsets.ViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    throttle_classes = [UserRateThrottle]
    parser_classes = [JSONParser]

    @extend_schema(tags=["Notifications"])
    def list(self, request):
        try:
            notifications = ns.get_notifications(request,Notification)
            serializer = NotificationSerializer(notifications, many=True)
            return MyResponse.success(data=serializer.data, message="Notifications retrieved.")
        except Exception as e:
            return MyResponse.failure(message="Failed to retrieve notifications.", status_code=500)


    @extend_schema(tags=["Notifications"])
    @action(detail=False, methods=['post'], url_path='mark-as-read')
    def mark_as_read(self, request):
        try:
            ids = request.data.get('ids')
            user_notifications = ns.filter_notifications(request,Notification)

            if ids:
                unread_qs = user_notifications.filter(id__in=ids, is_read=False)
            else:
                unread_qs = user_notifications.filter(is_read=False)

            updated_count = unread_qs.update(is_read=True)

            message = f"{updated_count} notification(s) marked as read." if updated_count else "No unread notifications found."
            return MyResponse.success(message=message)

        except Exception as e:
            return MyResponse.failure(message="Unable to mark notifications as read.", status_code=500)
