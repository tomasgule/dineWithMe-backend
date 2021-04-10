from rest_framework import generics
from rest_framework import status
from rest_framework import response
from rest_framework.response import Response
from django.core import serializers
from ..dinnerEvent.models import DinnerComment
from ..dinnerEvent.models import DinnerEvent
from rest_framework import viewsets
from rest_framework import permissions
from .serializers import AttendanceSerializer
from .serializers import DinnerEventSerializer
from .serializers import FilterPreferencesSerializer
from .permissions import IsHostOrAdminOrReadOnly
from .serializers import CommentSerializer


class DinnerEventViewSet(viewsets.ModelViewSet):
    permission_classes = [
        IsHostOrAdminOrReadOnly
    ]

    serializer_class = DinnerEventSerializer

    def get_queryset(self):
        return DinnerEvent.objects.all()

    def perform_create(self, serializers):
        serializers.save(host=self.request.user)

class DinnerCommentAPI(generics.GenericAPIView):
    serializer_class = CommentSerializer

    permission_classes = [
        permissions.IsAuthenticated
    ]
        
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = request.user

        print("this is request")
        print(request.data)
        print("this is validated_data")
        print(serializer.validated_data)
        
        comment = serializer.create(data=serializer.validated_data, user=user)
        comment.save()

        return Response(
            CommentSerializer(comment, context=self.get_serializer_context).data, status=status.HTTP_202_ACCEPTED
        )

class AttendanceAPI(generics.GenericAPIView):
    serializer_class = AttendanceSerializer
    
    permission_classes = [
        permissions.IsAuthenticated
    ]
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        dinner = serializer.validated_data  #Output fra serializer validate funksjonen antar vi
        
        if len(dinner.guests.all()) >= dinner.maxGuests:
            return Response("Maks gjester nådd", status=status.HTTP_400_BAD_REQUEST)
        
        if request.user == dinner.host:
            return Response("Bruker kan ikke melde seg på egen middag", status=status.HTTP_400_BAD_REQUEST)

        dinner.guests.add(request.user)
        dinner.save()
        
        return Response(
            "attending ok", status=status.HTTP_202_ACCEPTED
        )
    
    def delete(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        dinner = serializer.validated_data  #Output fra serializer validate funksjonen antar vi
        
        if len(dinner.guests.filter(username=request.user.username)) < 1:
            return Response("Kan ikke melde av bruker siden bruker ikke er påmeldt", status=status.HTTP_400_BAD_REQUEST)
        
        dinner.guests.remove(request.user)
        dinner.save()
        
        return Response("User removed from dinner",status=status.HTTP_202_ACCEPTED)
        
class FilterPreferencesAPI(generics.GenericAPIView):
    serializer = FilterPreferencesSerializer
    permission_classes = [
        permissions.AllowAny
    ]

    def get(self, request):
        serializer = self.serializer(data=request.data)
        serializer.is_valid()
        preferences = serializer.validated_data['preferences']
        data = DinnerEvent.objects.preference(preferences)
        s = DinnerEventSerializer(data=data, many=True)
        s.is_valid()
        data = serializers.serialize('json', data)
        return Response(data=s.data,status=status.HTTP_200_OK)

