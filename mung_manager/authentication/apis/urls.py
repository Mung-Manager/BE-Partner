from django.urls import path

from mung_manager.authentication.apis.api_managers import (
    JWTRefreshAPIManager,
    KakaoLoginAPIManager,
)

urlpatterns = [
    # auth
    path("/jwt/refresh", JWTRefreshAPIManager.as_view(), name="jwt-refresh"),
    # oauth
    path("/kakao/callback", KakaoLoginAPIManager.as_view(), name="kakao-login-callback"),
]
