from abc import ABC, abstractmethod

from django.db.models.query import QuerySet

from mung_manager.reservations.models import DailyReservation, DayOff, KoreaSpecialDay


class AbstractReservationSelector(ABC):
    @abstractmethod
    def check_is_exists_unpending_reservation_by_customer_id_and_customer_pet_id(
        self, customer_id: int, customer_pet_id: int
    ) -> bool:
        pass


class AbstractDailyReservationSelector(ABC):
    @abstractmethod
    def get_daily_reservations_queryset_by_year_and_month_and_pet_kindergarden_id(
        self, year: int, month: int, pet_kindergarden_id: int
    ) -> QuerySet[DailyReservation]:
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
