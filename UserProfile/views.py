from rest_framework import generics, permissions, status
from rest_framework.response import Response
from knox.models import AuthToken
from .serializers import UserSerializer, RegisterSerializer
from django.contrib.auth import login
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.views import LoginView as KnoxLoginView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth.models import User


class RegisterAPI(generics.GenericAPIView):
    '''
    Register a user - response contains token for authentication
    '''
    serializer_class = RegisterSerializer

    def post(self, request):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = serializer.save()
            return Response({
                "user": UserSerializer(user, context=self.get_serializer_context()).data,
                "token": AuthToken.objects.create(user)[1]
            })
        except IntegrityError:
            serializer.error_messages = {
                'username': 'A user with that username already exists!'}
            return Response(serializer.error_messages, status=status.HTTP_400_BAD_REQUEST)


class LoginAPI(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return super(LoginAPI, self).post(request, format=None)


@api_view(['DELETE'])
def delete_all_users(request):
    User.objects.all().filter(is_staff=False).delete()
    return Response({"response": "All non admin users where deletes"})
