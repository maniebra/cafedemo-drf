from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from yaml.serializer import SerializerError
from hashlib import sha256

from .models import User
import re

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

    def validate(self, data):
        if not re.match("[a-zA-Z]", data['first_name']):
            raise ValidationError("User's first name should consist only of english alphabet letters.")
        if not re.match("[a-zA-Z]", data['last_name']):
            raise ValidationError("User's last name should consist only of english alphabet letters.")
        # if not re.match("^\\+98[0-9]{12}$|^0[0-9]{12}$", data['phone_number']):
        #     raise ValidationError("Phone number should be of one of these two formats: 09123456789, +989123456789")
        # else:
        #     if re.match("^0[0-9]{12}$", data['phone_number']):
        #         data['phone_number'] = "+98" + data['phone_number'][1:]
        if not re.match("\\S+@\\S+.\\S+", data["email"]):
            raise ValidationError("Invalid email address.")

        return data