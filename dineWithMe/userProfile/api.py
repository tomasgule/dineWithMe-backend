from rest_framework import permissions
from rest_framework import generics
from knox.models import AuthToken
from .serializers import RegisterSerializers
from .serializers import UserProfileSerializer
from rest_framework.response import Response
from .serializers import UserProfileLogin

class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializers

    def post(self, request, *arg, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        userProfile = serializer.save()
        return Response({
            "userProfile": UserProfileSerializer(userProfile, context=self.get_serializer_context).data,
            "token": AuthToken.objects.create(userProfile)[1]
        })

class LoginAPI(generics.GenericAPIView):
    serializer_class = UserProfileLogin

    def post(self, request, *arg, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        userProfile = serializer.validated_data
        return Response({
            "userProfile": UserProfileSerializer(userProfile, context=self.get_serializer_context).data,
            "token": AuthToken.objects.create(userProfile)[1]
        })

class UserAPI(generics.RetrieveAPIView):
    permission_classes = [
        permissions.IsAuthenticated,
    ]
    serializer_class = UserProfileSerializer
    def get_object(self):
        return self.request.user

    
