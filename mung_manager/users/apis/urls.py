from django.urls import path

from mung_manager.users.apis.api_managers import UserProfileAPIManager

urlpatterns = [
    path(
        "/profile",
        UserProfileAPIManager.as_view(),
        name="user-profile",
    ),
]
