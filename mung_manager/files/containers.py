from dependency_injector import containers, providers

from mung_manager.files.services.files import FileUploadService


class FileContainer(containers.DeclarativeContainer):
    """이 클래스는 DI(Dependency Injection) 파일 컨테이너 입니다.

    Attributes:
        file_upload_service: 파일 업로드 서비스
    """

    file_upload_service = providers.Factory(FileUploadService)
