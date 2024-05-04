from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path

urlpatterns = [
    path("partner/api/v1/auth", include(("mung_manager.authentication.apis.urls", "api-auth"))),
    path("partner/api/v1/users", include(("mung_manager.users.apis.urls", "api-users"))),
    path("partner/api/v1/pet-kindergardens", include(("mung_manager.pet_kindergardens.apis.urls", "api-pet-kindergardens"))),
    path("partner/api/v1/files", include(("mung_manager.files.apis.urls", "api-files"))),
]

from config.settings.debug_toolbar.setup import DebugToolbarSetup  # noqa
from config.settings.swagger.setup import SwaggerSetup  # noqa

urlpatterns = DebugToolbarSetup.do_urls(urlpatterns)
urlpatterns = SwaggerSetup.do_urls(urlpatterns)

# Static/Media File Root (CSS, JavaScript, Images)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
