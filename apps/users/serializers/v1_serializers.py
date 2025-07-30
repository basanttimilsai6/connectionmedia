from rest_framework import serializers
from apps.users.models import User
import re

class UserSerializer(serializers.Serializer):
    full_name = serializers.CharField(required=True, allow_blank=False, max_length=100, error_messages={'required': 'Full name is required.', 'blank': 'Please enter your full name.'})
    email = serializers.EmailField(required=True, allow_blank=False, error_messages={'required': 'Email address is required.', 'blank': 'Please enter your email.', 'invalid': 'Enter a valid email address.'})
    contact_number = serializers.CharField(required=True, allow_blank=False, max_length=15, error_messages={'required': 'Contact number is required.', 'blank': 'Please enter your contact number.'})
    company_name = serializers.CharField(required=True, allow_blank=False, max_length=100, error_messages={'required': 'Company name is required.', 'blank': 'Please enter your company name.'})
    address = serializers.CharField(required=True, allow_blank=False, max_length=255, error_messages={'required': 'Address is required.', 'blank': 'Please enter your address.'})
    industry = serializers.CharField(required=True, allow_blank=False, max_length=100, error_messages={'required': 'Industry is required.', 'blank': 'Please enter your industry.'})
    username = serializers.CharField(required=True, allow_blank=False, max_length=150, error_messages={'required': 'Username is required.', 'blank': 'Please choose a username.'})
    password = serializers.CharField(write_only=True, required=True, allow_blank=False, min_length=8, error_messages={'required': 'Password is required.', 'blank': 'Please enter a password.', 'min_length': 'Password must be at least 8 characters long.'})


    def validate_email(self, value):
        email_regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        if not re.match(email_regex, value):
            raise serializers.ValidationError("Enter a valid email address.")
        return value
    
    def create(self,validated_data):
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user
    

class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True, allow_blank=False,error_messages={'required': 'Username is required.', 'blank': 'Please choose a username.'})
    password = serializers.CharField(required=True, allow_blank=False,error_messages={'required': 'Password is required.', 'blank': 'Please enter a password.', 'min_length': 'Password must be at least 8 characters long.'})
