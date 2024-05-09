from abc import ABC, abstractmethod


class AbstractFileUploadService(ABC):
    @abstractmethod
    def _validate_file_size(self):
        pass

    @abstractmethod
    def _validate_file_type(self):
        pass

    @abstractmethod
    def _get_resource_path(self) -> str:
        pass

    @abstractmethod
    def upload_file(self) -> str:
        pass
