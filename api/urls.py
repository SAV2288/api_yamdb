from django.urls import path
from django.urls import include

from rest_framework.routers import DefaultRouter

from api.views import TitleViewSet
from api.views import GenreViewSet
from api.views import CategoryViewSet


router = DefaultRouter()
router.register('titles', TitleViewSet)
router.register('genres', GenreViewSet)
router.register('categories', CategoryViewSet)

urlpatterns = [
    path('', include(router.urls)),
]