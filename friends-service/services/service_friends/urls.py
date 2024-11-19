from django.urls import include, path
from .views import (
    FavoriteUserView,
    FriendsListView,
    FriendRequestViewSet,
    FriendDeleteView,
)
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('', FriendsListView, basename='friends')

urlpatterns = [
    path("", include(router.urls)),
    path(
        "request/<int:user_id>/",
        FriendRequestViewSet.as_view({'post': 'create'}),
        name="friend-request"
    ),
    path(
        "approve_request/<int:user_id>/",
        FriendRequestViewSet.as_view({'post': 'approve'}),
        name="approve-friend-request"
    ),
    path(
        "delete/<int:user_id>/",
        FriendDeleteView.as_view(),
        name='friend-delete'
    ),
    path(
        "favorite/<int:user_id>/",
        FavoriteUserView.as_view(),
        name="add-to-favorite"
    ),
]
