from rest_framework import routers
from api.views import (
    CategoryViewSet,
    GenreViewSet,
    TitleViewSet)

router = routers.DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='categories'),
router.register(r'genres', GenreViewSet, basename='genres'),
router.register(r'titles', TitleViewSet, basename='titles')
