from abc import ABC, abstractmethod

from mung_manager.errors.exceptions import NotImplementedException


class AbstractFileUploadService(ABC):
    @abstractmethod
    def _validate_file_size(self):
        raise NotImplementedException()

    @abstractmethod
    def _validate_file_type(self):
        raise NotImplementedException()

    @abstractmethod
    def _get_resource_path(self) -> str:
        raise NotImplementedException()

    @abstractmethod
    def upload_file(self) -> str:
        raise NotImplementedException()
