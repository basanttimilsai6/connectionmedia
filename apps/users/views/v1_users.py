from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from apps.users.models import User
from apps.users.serializers.v1_serializers import UserSerializer,UserLoginSerializer
from core.response import MyResponse
from rest_framework.exceptions import ValidationError
from rest_framework.views import APIView
from apps.users.services.v1_services import UserServices as us


class UserRegistrationViewSet(viewsets.ViewSet):
    permission_classes = [AllowAny]
    serializer_class = UserSerializer

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
    serializer_class = UserLoginSerializer

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
        