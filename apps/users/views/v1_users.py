from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from apps.users.serializers.v1_serializers import UserSerializer,UserLoginSerializer
from core.response import MyResponse
from rest_framework.exceptions import ValidationError
from rest_framework.views import APIView
from apps.users.services.v1_services import UserServices as us
from rest_framework.throttling import AnonRateThrottle
from drf_spectacular.utils import extend_schema



class UserRegistrationViewSet(viewsets.ViewSet):
    permission_classes = [AllowAny]
    throttle_classes = [AnonRateThrottle]
    serializer_class = UserSerializer

    @extend_schema(tags=["Auth"])
    def create(self, request):
        try:
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = serializer.save()
            return MyResponse.success(message="User registered successfully!!", status_code=201)
        except ValidationError as ve:
            errors = ve.detail
            first_error = next(iter(errors.values()))[0]
            return MyResponse.failure(message=str(first_error))
        except Exception as e:
            return MyResponse.failure(message=f"Something went wrong {e}", status_code=500)

    

class UserLogin(APIView):
    permission_classes = [AllowAny]
    throttle_classes = [AnonRateThrottle]
    serializer_class = UserLoginSerializer

    @extend_schema(tags=["Auth"])
    def post(self,request):
        try:
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)
            token = us.get_token(serializer)
            data = {
                "refresh": str(token),
                "access": str(token.access_token),
                "expiration_in_seconds": us.get_access_token_in_seconds()
            }
            return MyResponse.success(message="Login successfully!!", data=data,status_code=201)
        except ValidationError as ve:
            errors = ve.detail
            first_error = next(iter(errors.values()))[0]
            return MyResponse.failure(message=str(first_error))
        except Exception as e:
            return MyResponse.failure(message=f"Something went wrong {e}", status_code=500)
        