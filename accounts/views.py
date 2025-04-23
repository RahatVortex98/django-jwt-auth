from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserRegisterSerializer,CustomTokenObtainPairSerializer
from .utils import send_verification_email
from rest_framework_simplejwt.views import TokenObtainPairView
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404
from .models import User



class RegisterView(APIView):
    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()
            send_verification_email(user, request)
            return Response({
                'message': "Registration successful! Please check your email to verify your account."
            }, status=status.HTTP_201_CREATED)

        return Response({'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)





class VerifyEmailView(APIView):
    def get(self, request, uidb64, token):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = get_object_or_404(User, id=uid)

            if default_token_generator.check_token(user, token):
                user.is_verified = True
                user.is_active = True  
                user.save()
                return Response({'message': 'Email verified successfully!'}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Invalid or expired token'}, status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as e:
            return Response({'error': 'Something went wrong'}, status=status.HTTP_400_BAD_REQUEST)


from rest_framework_simplejwt.views import TokenObtainPairView


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer




class LogoutView(APIView):
    def post(self, request):
        # The simplest logout mechanism: just remove the access token from the client
        # Here, we're not doing anything server-side because the JWT token doesn't need to be invalidated server-side
        # If you need server-side invalidation, you would implement token blacklisting

        # A response with a success message
        return Response({"message": "You have been logged out successfully."}, status=status.HTTP_200_OK)