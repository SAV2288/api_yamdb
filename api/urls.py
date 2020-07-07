from django.urls import path, include
from rest_framework.routers import DefaultRouter

from api.views import ReviewViewSet, CommentViewSet, TitleViewSet, GenreViewSet, CategoryViewSet


router = DefaultRouter()

router.register('titles', TitleViewSet)
router.register('genres', GenreViewSet)
router.register('categories', CategoryViewSet)
router.register(r'/titles/(?P<title_id>\d+)/reviews/', ReviewViewSet)
router.register(r'/titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments', CommentViewSet)

urlpatterns = [

        path('', include(router.urls)),
    ]
