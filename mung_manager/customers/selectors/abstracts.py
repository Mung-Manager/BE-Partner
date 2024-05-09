from abc import ABC, abstractmethod
from typing import List, Optional

from django.db.models.query import QuerySet

from mung_manager.customers.models import (
    Customer,
    CustomerPet,
    CustomerTicket,
    CustomerTicketReservation,
)


class AbstractCustomerSelector(ABC):
    @abstractmethod
    def get_customer_list(self, filters: Optional[dict] = None) -> QuerySet[Customer]:
        pass

    @abstractmethod
    def get_customer_by_id(self, customer_id: int) -> Optional[Customer]:
        pass

    @abstractmethod
    def get_customer_with_undeleted_customer_pet_by_id(
        self, customer_id: int
    ) -> Optional[Customer]:
        pass

    @abstractmethod
    def check_is_exists_customer_by_id(self, customer_id: int) -> bool:
        pass

    @abstractmethod
    def check_is_exists_customer_by_pet_kindergarden_id_and_phone_number(
        self, pet_kindergarten_id: int, phone_number: str
    ) -> bool:
        pass

    @abstractmethod
    def get_customer_queryset_by_pet_kindergarden_id(
        self, pet_kindergarten_id: int
    ) -> QuerySet[Customer]:
        pass


class AbstractCustomerTicketSelector(ABC):
    @abstractmethod
    def get_customer_ticket_with_ticket_queryset_by_customer_id(
        self, customer_id: int
    ) -> QuerySet[CustomerTicket]:
        pass


class AbstractCustomerTicketReservationSelector(ABC):
    @abstractmethod
    def get_customer_ticket_reservation_list_by_customer_id(
        self, customer_id: int
    ) -> QuerySet[CustomerTicketReservation]:
        pass


class AbstractCustomerPetSelector(ABC):
    @abstractmethod
    def get_undeleted_customer_pet_queryset_by_names_and_customer_id(
        self, names: List[str], customer_id: int
    ) -> QuerySet[CustomerPet]:
        pass

    @abstractmethod
    def check_is_exists_undeleted_customer_pet_by_names_and_customer_id(
        self, names: List[str], customer_id: int
    ) -> bool:
        pass
