from rest_framework import serializers
from .models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=68, min_length=8, write_only=True)
    password2 = serializers.CharField(max_length=68, min_length=8, write_only=True)

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'password', 'password2']

    def validate(self, attrs):
        """
        Check that the passwords match.
        """
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Passwords must match."})
        
        # Validate the password strength using Django's default password validators
        validate_password(attrs['password'])
        
        return attrs

    def create(self, validated_data):
        """
        Create a new user and return it.
        """
        validated_data.pop('password2')  # Remove password2 since it's not needed anymore
        user = User.objects.create_user(**validated_data)  # Use the custom manager to create the user
        return user





class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        if not self.user.is_verified:
            raise serializers.ValidationError("Your email is not verified yet.")

        return data
