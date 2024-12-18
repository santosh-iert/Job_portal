# Serializer for User Registration
import re
from rest_framework import serializers
from users.models import CustomUser


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)


    class Meta:
        model = CustomUser
        fields = ['email', 'password', 'phone_number', 'first_name', 'last_name', 'user_type']



    def create(self, validated_data):
        if 'username' not in validated_data:
            validated_data['username'] = f"@{validated_data['email'].split('@')[0]}"
        user = CustomUser.objects.create_user(**validated_data)
        return user


    def validate_password(self, value):
        if not bool(re.match(pattern=r'^.{8,}$', string=value)):
            raise ValueError('Password must be at least 8 Character')
        if not bool(re.search(pattern=r'[A-Z]', string=value)):
            raise ValueError('Password must be at least 1 upper Character')
        if not bool(re.search(pattern=r'[a-z]', string=value)):
            raise ValueError('Password must be at least 1 lower Character')
        if not bool(re.search(pattern=r'[!@#$%^&*(),.?":{}|<>]', string=value)):
            raise ValueError('Password must be at least special Character')
        return value

