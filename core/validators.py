import re
from django.core.exceptions import ValidationError
from django.core.validators import validate_email

def validate_phone_number(value):
    """Validate Nepali phone number format: +977-98XXXXXXXX"""
    phone_regex = re.compile(r'^\+977\-\d{10}$')
    if not phone_regex.match(value):
        raise ValidationError('Invalid phone number format. Format must be +977-XXXXXXXXXX')

def validate_strong_password(value):
    """Validate password strength"""
    if len(value) < 8:
        raise ValidationError('Password must be at least 8 characters long')
    
    if not re.search(r'[A-Z]', value):
        raise ValidationError('Password must contain at least one uppercase letter')
    
    if not re.search(r'[a-z]', value):
        raise ValidationError('Password must contain at least one lowercase letter')
    
    if not re.search(r'\d', value):
        raise ValidationError('Password must contain at least one digit')