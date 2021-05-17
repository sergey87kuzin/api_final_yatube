from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

from .views import CommentViewSet, FollowViewSet, GroupViewSet, PostViewSet

router_v1 = DefaultRouter()
router_v1.register(r'posts', PostViewSet, basename='posts')
router_v1.register(r'posts/(?P<post_id>[0-9]+)/comments',
                   CommentViewSet, basename='comments')
router_v1.register(r'follow', FollowViewSet, basename='follows')
router_v1.register(r'group', GroupViewSet, basename='groups')

v1_patterns = [
    path('', include(router_v1.urls)),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(),
         name='token_refresh'),
]

urlpatterns = [
    path('v1/', include(v1_patterns)),
]
