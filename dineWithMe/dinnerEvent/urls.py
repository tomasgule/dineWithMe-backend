from rest_framework import routers
from .api import DinnerEventViewSet
from .api import AttendanceAPI
from .api import FilterPreferencesAPI
from .api import DinnerCommentAPI
from django.urls import path, include

router = routers.DefaultRouter()
router.register('api/dinnerEvent', DinnerEventViewSet, 'dinnerEvent')


urlpatterns = [
    path('', include(router.urls)),
    path('api/attend', AttendanceAPI.as_view()),
    path('api/dinnerEvent/filter', FilterPreferencesAPI.as_view()),
    path('api/comment', DinnerCommentAPI.as_view())
]

