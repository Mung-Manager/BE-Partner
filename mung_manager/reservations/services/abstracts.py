from abc import ABC, abstractmethod

from mung_manager.reservations.models import DayOff, Reservation


class AbstractDayOffService(ABC):
    @abstractmethod
    def create_day_off(self, pet_kindergarden_id: int, day_off_at: str, user) -> DayOff:
        pass

    @abstractmethod
    def delete_day_off(self, pet_kindergarden_id: int, day_off_id: int, user) -> None:
        pass


class AbstractReservationService(ABC):
    @abstractmethod
    def toggle_reservation_is_attended(self, pet_kindergarden_id: int, reservation_id: int, user) -> Reservation:
        pass
