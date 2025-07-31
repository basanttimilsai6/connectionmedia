from rest_framework import viewsets,permissions
from rest_framework.permissions import AllowAny
from apps.users.serializers.v1_serializers import UserSerializer,UserLoginSerializer,UserSearchSerializer
from core.response import MyResponse
from rest_framework.exceptions import ValidationError
from rest_framework.views import APIView
from apps.users.services.v1_services import UserServices as us
from rest_framework.throttling import AnonRateThrottle,UserRateThrottle
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.filters import SearchFilter
from drf_spectacular.utils import extend_schema
from apps.users.models import User
from django.db.models import Q



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


class UserSearchView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    throttle_classes = [UserRateThrottle]
    serializer_class = UserSerializer

    @extend_schema(parameters=[UserSearchSerializer],tags=["User Filters"])
    def get(self, request):
        try:
            filters = {
                'full_name__icontains': request.query_params.get('name'),
                'email__icontains': request.query_params.get('email'),
                'contact_number__icontains': request.query_params.get('phone'),
                'company_name__icontains': request.query_params.get('company'),
            }
            # Remove None values
            filters = {k: v for k, v in filters.items() if v}

            queryset = User.objects.filter(**filters) if filters else User.objects.all()

            serializer = self.serializer_class(queryset, many=True)
            return MyResponse.success(
                message="Users fetched successfully.",
                data=serializer.data,
                status_code=200
            )
        except Exception as e:
            return MyResponse.failure(
                message=f"Something went wrong: {str(e)}",
                status_code=500
            )