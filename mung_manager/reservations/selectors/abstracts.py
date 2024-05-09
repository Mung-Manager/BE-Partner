from abc import ABC, abstractmethod


class AbstractReservationSelector(ABC):
    @abstractmethod
    def check_is_exists_unpending_reservation_by_customer_id_and_customer_pet_id(
        self, customer_id: int, customer_pet_id: int
    ) -> bool:
        pass
