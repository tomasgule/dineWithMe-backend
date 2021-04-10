from rest_framework import serializers
from .models import DinnerEvent
from .models import DinnerPreferences
from .models import DinnerPreferences
from .models import DinnerComment
from ..userProfile.serializers import UserProfileSerializer
from ..userProfile.serializers import UserNameSerializer


class DinnerPreferencesSerializer(serializers.ModelSerializer):
    class Meta:
        model = DinnerPreferences
        fields = ["preference"]


class CommentSerializer(serializers.ModelSerializer):
    dinner_id = serializers.IntegerField(write_only=True)
    user = UserNameSerializer(read_only=True)

    class Meta:
        model = DinnerComment
        fields = "__all__"

    def create(self, data, user):
        dinner = DinnerEvent.objects.get(id=data.pop("dinner_id")) 
        return DinnerComment.objects.create(user=user, dinner_id=dinner, **data)


class DinnerEventSerializer(serializers.ModelSerializer):
    host = UserProfileSerializer(read_only=True)
    preferences = DinnerPreferencesSerializer(
        many=True, allow_empty=True, required=False
    )
    comment = CommentSerializer(
        many=True, read_only=True, allow_empty=True, required=False
    )
    guests = UserProfileSerializer(read_only=True, many=True)

    class Meta:
        model = DinnerEvent
        fields = "__all__"
        extra_kwargs = {"guests": {"read_only": True}}

    def create(self, data):
        try:
            preferences = data.pop("preferences")
        except:
            preferences = []
        try:
            comment = data.pop("comment")
        except:
            comment = []
        dinner = DinnerEvent.objects.create(**data)
        for preference in preferences:
            DinnerPreferences.objects.create(**preference, dinner_id=dinner)
        for comment in comment:
            DinnerComment.objects.create(**comment, dinner_id=dinner)
        return dinner

    def update(self, instance, data):
        try:
            preferences = data.pop("preferences")
        except:
            preferences = []
        dinner, created = DinnerEvent.objects.update_or_create(
            id=instance.id, defaults=data
        )
        for preference in preferences:
            DinnerPreferences.objects.update_or_create(**preference, dinner_id=dinner)
        return dinner


class AttendanceSerializer(serializers.Serializer):
    dinner_id = serializers.IntegerField()

    def validate(self, data):
        dinner = DinnerEvent.objects.filter(pk=data["dinner_id"])

        if len(dinner) == 1:
            return dinner[0]
        raise serializers.ValidationError("Dinner does not exist")


class FilterPreferencesSerializer(serializers.Serializer):
    preferences = serializers.ListField(child=serializers.CharField(max_length=50))
