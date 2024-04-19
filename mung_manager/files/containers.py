from dependency_injector import containers, providers

from mung_manager.files.services.files import FileUploadService


class FileContainer(containers.DeclarativeContainer):
    """이 클래스는 DI(Dependency Injection) 파일 컨테이너 입니다.

    Attributes:
        ticket_selector: 티켓 셀렉터
        pet_kindergarden_selector: 펫 킨더가든 셀렉터
        ticket_service: 티켓 서비스
    """

    file_upload_service = providers.Factory(FileUploadService)
