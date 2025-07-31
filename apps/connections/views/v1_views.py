from rest_framework import viewsets, permissions
from rest_framework.exceptions import PermissionDenied
from rest_framework.decorators import action
from django.db.models import Q
from apps.connections.models import ConnectionRequests
from apps.connections.serializers.v1_serializers import (
    ConnectionRequestSerializer,
    ConnectionCreateSerializer,
    ConnectionStatusUpdateSerializer,
)
from rest_framework.throttling import UserRateThrottle
from rest_framework_simplejwt.authentication import JWTAuthentication
from core.response import MyResponse
from drf_spectacular.utils import extend_schema

class ConnectionRequestViewSet(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    throttle_classes = [UserRateThrottle]

    def get_queryset(self):
        user = self.request.user
        return ConnectionRequests.objects.filter(
            Q(sender=user) | Q(receiver=user)
        ).select_related('sender', 'receiver')

    def get_serializer_class(self):
        if self.action == 'create':
            return ConnectionCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return ConnectionStatusUpdateSerializer
        return ConnectionRequestSerializer

    @extend_schema(tags=["Connections"])
    def list(self, request, *args, **kwargs):
        try:
            queryset = self.filter_queryset(self.get_queryset())
            serializer = self.get_serializer(queryset, many=True)
            return MyResponse.success(data=serializer.data, message="Connection list fetched")
        except Exception as e:
            return MyResponse.failure(message=str(e))
        

    @extend_schema(tags=["Connections"])
    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            return MyResponse.success(data=serializer.data, message="Connection details fetched")
        except Exception as e:
            return MyResponse.failure(message=str(e))


    @extend_schema(tags=["Connections"])
    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            return MyResponse.success(data=serializer.data, message="Connection request sent", status_code=201)
        except Exception as e:
            return MyResponse.failure(message=str(e))

    @extend_schema(tags=["Connections"])
    def partial_update(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            if instance.receiver != request.user:
                raise PermissionDenied("Only the receiver can update the connection status.")
            serializer = self.get_serializer(instance, data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return MyResponse.success(data=serializer.data, message="Connection status updated")
        except PermissionDenied as e:
            return MyResponse.failure(message=str(e), status_code=403)
        except Exception as e:
            return MyResponse.failure(message=str(e))
        
    @extend_schema(tags=["Connections"])
    def update(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            if instance.receiver != request.user:
                raise PermissionDenied("Only the receiver can update the connection status.")
            serializer = self.get_serializer(instance, data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return MyResponse.success(data=serializer.data, message="Connection status updated")
        except PermissionDenied as e:
            return MyResponse.failure(message=str(e), status_code=403)
        except Exception as e:
            return MyResponse.failure(message=str(e))


    @extend_schema(tags=["Connections"])
    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            if request.user != instance.sender and request.user != instance.receiver:
                raise PermissionDenied("Only sender or receiver can delete this request.")
            self.perform_destroy(instance)
            return MyResponse.success(message="Connection request deleted", data={})
        except PermissionDenied as e:
            return MyResponse.failure(message=str(e), status_code=403)
        except Exception as e:
            return MyResponse.failure(message=str(e))

    @extend_schema(tags=["Connections"])
    @action(detail=True, methods=['post'])
    def accept(self, request, pk=None):
        try:
            instance = self.get_object()
            if instance.receiver != request.user:
                raise PermissionDenied("Only the receiver can accept the request.")
            instance.status = 'accepted'
            instance.save()
            return MyResponse.success(message="Connection accepted")
        except PermissionDenied as e:
            return MyResponse.failure(message=str(e), status_code=403)
        except Exception as e:
            return MyResponse.failure(message=str(e))


    @extend_schema(tags=["Connections"])
    @action(detail=True, methods=['post'])
    def reject(self, request, pk=None):
        try:
            instance = self.get_object()
            if instance.receiver != request.user:
                raise PermissionDenied("Only the receiver can reject the request.")
            instance.status = 'rejected'
            instance.save()
            return MyResponse.success(message="Connection rejected")
        except PermissionDenied as e:
            return MyResponse.failure(message=str(e), status_code=403)
        except Exception as e:
            return MyResponse.failure(message=str(e))
