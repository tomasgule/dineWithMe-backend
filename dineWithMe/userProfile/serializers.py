from .models import UserProfile
from rest_framework import serializers
from django.contrib.auth import authenticate

class RegisterSerializers(serializers.ModelSerializer):

    class Meta:
        model = UserProfile
        fields = ('id','first_name','last_name','username', 'email', 'password', 'birthday','phoneNumber','allergy','gender','bio')
        extra_kwargs = {'password':{'write_only':True}}
    
    def create(self, validated_data):
        userProfile = UserProfile.objects.create_user(**validated_data)
        userProfile.save()
        return userProfile

class UserProfileSerializer(serializers.ModelSerializer):
     class Meta:
        model = UserProfile
        fields = ('id', 'username','first_name','last_name', 'email', 'birthday','phoneNumber','allergy','gender','bio')

class UserNameSerializer(serializers.ModelSerializer):
     class Meta:
        model = UserProfile
        fields = ('username', 'first_name','last_name')

class UserProfileLogin(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Incorrect Credentials")



    
