from rest_framework import serializers
from .models import CustomUser
from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils.translation import gettext_lazy as _
from .models import CustomUser



class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'first_name', 'last_name']


class UserSignupSerializers(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'email', 'password', 'password2')
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "password fields didn't match."})
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('password2')
        user = CustomUser.objects.create_user(**validated_data)
        return user
    


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    
    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        # Authenticate the user
        user = authenticate(username=email, password=password)

        if user:
            if not user.is_active:
                msg = _('User account is disabled.')
                raise serializers.ValidationError(msg)

            if hasattr(user, 'profile') and user.profile.role < 2:
                msg = _("You are not allowed to login")
                raise serializers.ValidationError(msg)

            refresh = RefreshToken.for_user(user)
            user_data = CustomUserSerializer(user).data

            return {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': user_data
            }
        else:
            msg = _('Unable to log in with provided credentials.')
            raise serializers.ValidationError(msg)