from abc import ABC, abstractmethod
from typing import Optional

from django.db.models.query import QuerySet

from mung_manager.pet_kindergardens.models import PetKindergarden, RawPetKindergarden


class AbstractPetKindergardenSelector(ABC):
    @abstractmethod
    def check_is_exists_pet_kindergarden_by_user(self, user) -> bool:
        pass

    @abstractmethod
    def get_pet_kindergarden_by_user(self, user) -> Optional[PetKindergarden]:
        pass

    @abstractmethod
    def check_is_exists_pet_kindergarden_by_id_and_user(self, pet_kindergarten_id: int, user) -> bool:
        pass


class AbstractRawPetKindergardenSelector(ABC):
    @abstractmethod
    def get_raw_pet_kindergarden_queryset_by_name(self, name: str) -> QuerySet[RawPetKindergarden]:
        pass
