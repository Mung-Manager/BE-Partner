from abc import ABC, abstractmethod
from typing import Optional

from django.db.models.query import QuerySet

from mung_manager.pet_kindergardens.models import (
    DayOff,
    KoreaSpecialDay,
    PetKindergarden,
    RawPetKindergarden,
)


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


class AbstractDayOffSelector(ABC):
    @abstractmethod
    def get_day_off_queryset_by_pet_kindergarden_id_and_day_off_at(
        self, pet_kindergarden_id: int, year: int, month: int
    ) -> QuerySet[DayOff]:
        pass


class AbstractKoreaSpecialDaySelector(ABC):
    @abstractmethod
    def get_korea_special_day_queryset_by_year_and_month(self, year: int, month: int) -> QuerySet[KoreaSpecialDay]:
        pass
