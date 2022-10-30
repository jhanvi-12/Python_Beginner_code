from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from star_studio.constants import PASSWORD_NOT_MATCH, INVALID_LOGIN_CREDENTIAL, USER_ALREADY_EXISTS
from star_studio.models import User


class RegisterSerializer(serializers.ModelSerializer):
    """serializer for creating user """
    username = serializers.CharField(required=True)
    email = serializers.EmailField(required=True, validators=[UniqueValidator(queryset=User.objects.all())])
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    confirm_password = serializers.CharField(write_only=True, required=True)
    phone_number = serializers.IntegerField(required=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'confirm_password', 'phone_number']
        extra_kwargs = {
            'username': {'required': True},
            'email': {'required': True}
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError(
                {'password': PASSWORD_NOT_MATCH}
            )
        return attrs

    def create(self, validated_data):
        """method for register the user"""
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            phone_number=validated_data['phone_number'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class LoginSerializer(serializers.ModelSerializer):
    """
    user login serializer
    """
    email = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ['id', 'email', 'password']

    def validate(self, attrs):
        email = attrs.get('email', None)
        password = attrs.get('password', None)
        username = User.objects.get(email=email).username
        user = authenticate(username=username, password=password)
        if not user:
            raise serializers.ValidationError({'invalid credential': INVALID_LOGIN_CREDENTIAL})
        if not user.check_password(password):
            raise serializers.ValidationError("Invalid Password")
        attrs['user'] = user
        return attrs


class ChangePasswordSerializer(serializers.Serializer):
    """serializer for change password from old_password"""
    old_password = serializers.CharField()
    new_password = serializers.CharField()


class UserSerializer(serializers.ModelSerializer):
    """
    serializer for user that serialize :
    ('id', 'first_name', 'last_name' , 'email', 'image',
    'is_active', 'is_superuser' /)
    """
    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'email',
            'password',
            'phone_number'
        ]
        extra_kwargs = {
            'phone_number': {'read_only': True}
        }


class DeleteUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User