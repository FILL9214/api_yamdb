from rest_framework import routers
from django.urls import include, path
from api.views import (
    CategoryViewSet,
    GenreViewSet,
    TitleViewSet,
    CommentViewSet,
    ReviewViewSet,
    SignUpViewSet,
    TokenViewSet,
    UsersViewSet
)

router = routers.DefaultRouter()
router.register('users', UsersViewSet, basename='users')
router.register(r'categories', CategoryViewSet, basename='categories'),
router.register(r'genres', GenreViewSet, basename='genres'),
router.register(r'titles', TitleViewSet, basename='titles')
router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet, basename='reviews')
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet, basename='comments'
)

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/auth/token/', TokenViewSet.as_view(), name='get_token'),
    path('v1/auth/signup/', SignUpViewSet.as_view(), name='signup'),
]
