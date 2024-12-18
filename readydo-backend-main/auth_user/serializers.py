from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from auth_user.models import User
from common.serializers import BaseSerializer


class TokenCredentialsSerializer(TokenObtainPairSerializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not kwargs.get('data'):  # Just for Swagger
            self.fields['phone_number'] = serializers.CharField(required=False)
            self.fields['email'] = serializers.CharField(required=False)


class UserModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email', 'phone_number', 'username', 'avatar')
        read_only_fields = ('id', 'email', 'is_admin')


class RegisterSerializer(serializers.ModelSerializer):
    middle_name = serializers.CharField(max_length=20, allow_blank=True)
    avatar = serializers.FileField(required=False)
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        exclude = ['created_at', 'is_superuser', 'is_admin', 'is_active', 'is_staff', 'language', 'groups', 'user_permissions', 'last_login', 'following', 'grade']


class SendSMSEmailSerializer(BaseSerializer):
    email = serializers.EmailField(max_length=30, required=True)


class PasswordVarifyCodeSerializer(BaseSerializer):
    token = serializers.CharField(max_length=32, required=True)
    code = serializers.CharField(max_length=4, required=True)
    password = serializers.CharField(max_length=30, required=True)


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ['is_admin', 'is_active', 'is_staff', 'created_at', 'language', 'groups', 'user_permissions', 'password', 'following']

        extra_kwargs = {
            'password': {'required': False},
            'email': {'required': False},
            'first_name': {'required': False},
            'last_name': {'required': False},
            'phone_number': {'required': False},
            'grade' : {'read_only': True}
        }
