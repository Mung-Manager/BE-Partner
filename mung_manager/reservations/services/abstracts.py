from abc import ABC, abstractmethod

from mung_manager.reservations.models import DayOff


class AbstractDayOffService(ABC):
    @abstractmethod
    def create_day_off(self, pet_kindergarden_id: int, day_off_at: str, user) -> DayOff:
        pass

    @abstractmethod
    def delete_day_off(self, pet_kindergarden_id: int, day_off_id: int, user) -> None:
        pass
