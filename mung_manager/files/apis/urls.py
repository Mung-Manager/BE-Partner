from django.urls import path

from mung_manager.files.apis.api_managers import FileUploadAPIManager

urlpatterns = [
    path("/upload", FileUploadAPIManager.as_view(), name="file-upload"),
]
