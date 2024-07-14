from rest_framework.generics import GenericAPIView
from .serializers import RegisterUserSerializer, LoginUserSerializer
from rest_framework.response import Response
from rest_framework import status, permissions
from django.contrib.auth import authenticate

# Create your views here.

class AuthUserAPIView(GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    def get(self, request):
        user = request.user
        
        serializer = RegisterUserSerializer(user)
        return Response({
            'user':serializer.data
        })

class RegisterApiView(GenericAPIView):
    serializer_class = RegisterUserSerializer
    authentication_classes = []
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginAPIView(GenericAPIView):
    authentication_classes = []
    serializer_class = LoginUserSerializer
    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")
        
        user = authenticate(username=email, password=password)
        if user:
            serializer = self.serializer_class(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({
                "message": "Invalid credentials, try again"
            }, status=status.HTTP_401_UNAUTHORIZED)
                