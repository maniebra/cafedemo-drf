from rest_framework import serializers
from rest_framework.exceptions import ValidationError
import re
from rest_framework import serializers
from backend.cafedemo.users.models import User

def user_validation(data):
    if not re.match("[a-zA-Z]", data['first_name']):
        raise ValidationError("User's first name should consist only of english alphabet letters.")
    if not re.match("[a-zA-Z]", data['last_name']):
        raise ValidationError("User's last name should consist only of english alphabet letters.")
    if not re.match("\\S+@\\S+.\\S+", data["email"]):
        raise ValidationError("Invalid email address.")

    return data

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

    def validate(self, data):
        return user_validation(data)

class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'phone_number', 'email', 'password']

    def validate(self, data):
        return user_validation(data)