from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.views import View
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from .models import CustomUser
from .serializers import UserSignupSerializers, LoginSerializer
from rest_framework.permissions import AllowAny



class SignUpView(CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSignupSerializers
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response({"message": "User created successfully"}, status=status.HTTP_201_CREATED, headers=headers)
    

class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.validated_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        logout(request)  
        return Response({"message": "Logged out successfully"}, status=status.HTTP_200_OK)
    