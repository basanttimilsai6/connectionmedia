from django.contrib.auth import authenticate
from core.token import get_tokens_for_user
from rest_framework.exceptions import AuthenticationFailed
from configurations.settings.base import SIMPLE_JWT,ACCESS_TOKEN_LIFETIME

class UserServices:
    @staticmethod
    def get_token(serializer):
        username = serializer.validated_data["username"]
        password = serializer.validated_data["password"]

        # Authenticate user
        user = authenticate(username=username, password=password)

        if user is None:
            raise AuthenticationFailed("Invalid username or password.")

        return get_tokens_for_user(user)
    
    def get_access_token_in_seconds():
        return str(SIMPLE_JWT["ACCESS_TOKEN_LIFETIME"].total_seconds())