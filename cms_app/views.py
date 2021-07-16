from django.shortcuts import render
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import Group
from django.views.generic.base import View
from rest_framework import serializers, status
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework import filters
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import UserRegister
from .serializers import UserDetailSerializer, UserRegisterSerializer, LoginSerializer
from .permissions import UpdateOwnContent, AdminOnly
from rest_framework.generics import RetrieveAPIView, CreateAPIView


class RegisterUserView(CreateAPIView):
    permission_classes = ([AllowAny])
    serializer_class = UserRegisterSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        status_code = status.HTTP_201_CREATED
        response = {
            'success' : 'True',
            'status code' : status_code,
            'message': 'User registered  successfully',
            }
        
        return Response(response, status=status_code)


class LoginView(RetrieveAPIView):
    permission_classes = ([AllowAny])
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        response = {
            'success' : 'True',
            'status code' : status.HTTP_200_OK,
            'message': 'User logged in  successfully',
            'token' : serializer.data['token'],
            }
        status_code = status.HTTP_200_OK

        return Response(response, status=status_code)


class LogoutView(APIView):
    permission_classes = [(IsAuthenticated)]
    serailizer_class = LoginSerializer

    def post(self, request):
        token = request.auth
        # print(token)
        try: 
            token = Token.objects.get(key=token).delete()
            logout(request)
        except:
            return Response({"error": "session1 does not exists."}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"message": "Successfully logged out."}, status=status.HTTP_200_OK)


class UserDetailsView(APIView):
    # permission_classes = (IsAuthenticated,)
    serializer_class = UserDetailSerializer
    # filter_backends = (filters.SearchFilter,)
    # search_fields = ('email', 'address', 'username')
    
    def get(self, request):
        qs = UserRegister.objects.all()
        serializer = self.serializer_class(qs, many=True)
        return Response(serializer.data)

    def patch(self, request, pk=None):
        if request.user.id == pk:
            user = UserRegister.objects.filter(pk=pk).first()
            serializer = self.serializer_class(user, data=request.data, partial=True)
            if serializer.is_valid():
                # print('-----here-----',serializer.data)
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error": "Unauthorized!"}, status=status.HTTP_401_UNAUTHORIZED)