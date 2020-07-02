from django.urls import path, include
from rest_framework.routers import DefaultRouter

from api.views import ReviewViewSet, CommentViewSet


router = DefaultRouter()

router.register(r'/titles/(?P<title_id>\d+)/reviews/', ReviewViewSet)
router.register(r'/titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments', CommentViewSet)

urlpatterns = [

        path('', include(router.urls)),
    ]