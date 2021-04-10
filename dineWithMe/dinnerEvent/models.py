from django.db import models
from django.core.validators import MinValueValidator
from ..userProfile.models import UserProfile

# Create your models here.
class DinnerPreferencesManager(models.Manager):
    def preference(self, preferences):
        dinners = DinnerEvent.objects.all()
        for preference in preferences:
            dinners = dinners.filter(preferences__preference=preference)
        return dinners


class DinnerEvent(models.Model):
    header = models.CharField(max_length=100)
    dateTime = models.DateTimeField()
    address = models.CharField(max_length=100)
    description = models.TextField(max_length=500)
    price = models.DecimalField(
        decimal_places=2, max_digits=6, null=True, validators=[MinValueValidator(0.0)]
    )
    host = models.ForeignKey(
        UserProfile, related_name="dinnerEvent", on_delete=models.CASCADE, null=True
    )
    maxGuests = models.PositiveSmallIntegerField()
    guests = models.ManyToManyField(UserProfile, related_name="attending")
    is_cancelled = models.BooleanField(null=True)
    
    objects = DinnerPreferencesManager()


FOOD_PREFERENCES = [
    ("vegetarian", "vegetarian"),
    ("vegan", "vegan"),
    ("no_egg", "no_egg"),
    ("gluten_free", "gluten_free"),
    ("lactose_free", "lactose_free"),
    ("no_nut", "no_nut")
]


class DinnerPreferences(models.Model):
    dinner_id = models.ForeignKey(
        DinnerEvent, related_name="preferences", on_delete=models.CASCADE
    )
    preference = models.CharField(max_length=50, choices=FOOD_PREFERENCES)

    class Meta:
        unique_together = ("dinner_id", "preference")


class DinnerComment(models.Model):
    dinner_id = models.ForeignKey(
        DinnerEvent, related_name="comment", on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        UserProfile, related_name="comment", on_delete=models.CASCADE
    )
    text = models.CharField(max_length=600)
    created_at = models.DateTimeField(auto_now_add=True)
