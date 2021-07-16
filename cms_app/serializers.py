import django.contrib.auth.password_validation as validators
from rest_framework import serializers
from .models import UserRegister
from rest_framework_jwt.settings import api_settings
from django.contrib.auth import authenticate
from django.contrib.auth.models import update_last_login
from django.contrib.auth.models import User


JWT_PAYLOAD_HANDLER = api_settings.JWT_PAYLOAD_HANDLER
JWT_ENCODE_HANDLER = api_settings.JWT_ENCODE_HANDLER


class UserRegisterSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = UserRegister
        fields = ('id', 'email', 'username', 'password', 'address')
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate_password(self, data):
        min_length=1
        
        # print(data)
        special_characters = "[~\!@#\$%\^&\*\(\)_\+{}\":;'\[\]]"
        if len(data) < 8:
            raise serializers.ValidationError(('Password must contain at least 8 letters'))
        if not any(char.isdigit() for char in data):
            raise serializers.ValidationError(('Password must contain at least %(min_length)d digit.') % {'min_length': min_length})
        if not any(char.isalpha() for char in data):
            raise serializers.ValidationError(('Password must contain at least %(min_length)d letter.') % {'min_length': min_length})
        if not any(char in special_characters for char in data):
            raise serializers.ValidationError(('Password must contain at least %(min_length)d special character.') % {'min_length': min_length})
        return data

    def save(self):
        data = UserRegister(
            email=self.validated_data['email'],
            username=self.validated_data['username'],
            address=self.validated_data['address'],
        )
        password=self.validated_data['password']
        data.set_password(password)
        data.save()
        return data


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(
        style={'input_type': 'password'}, write_only=True, required=True
    )
    token = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):
        email = data.get("email", None)
        password = data.get("password", None)
        user = authenticate(email=email, password=password)
        if user is None:
            raise serializers.ValidationError(
                'A user with this email and password is not found.'
            )
        try:
            payload = JWT_PAYLOAD_HANDLER(user)
            print('payload---------', payload)
            jwt_token = JWT_ENCODE_HANDLER(payload)
            print('jwt_token-------', jwt_token)
            update_last_login(None, user)
        except User.DoesNotExist:
            raise serializers.ValidationError(
                'User with given email and password does not exists'
            )
        return {
            'email':user.email,
            'token': jwt_token
        }

    class Meta:
        model = UserRegister
        fields = (
            'email',
            'password'
        )

class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserRegister
        fields = ('id', 'email', 'username', 'password', 'address')
        extra_kwargs = {
            'password': {'write_only': True}
        }
