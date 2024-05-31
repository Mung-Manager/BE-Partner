from abc import ABC, abstractmethod
from typing import List, Optional

from django.db.models.query import QuerySet

from mung_manager.customers.models import (
    Customer,
    CustomerPet,
    CustomerTicket,
    CustomerTicketReservation,
)
from mung_manager.errors.exceptions import NotImplementedException


class AbstractCustomerSelector(ABC):
    @abstractmethod
    def get_customer_list(self, filters: Optional[dict] = None) -> QuerySet[Customer]:
        raise NotImplementedException()

    @abstractmethod
    def get_customer_by_id(self, customer_id: int) -> Optional[Customer]:
        raise NotImplementedException()

    @abstractmethod
    def get_customer_with_undeleted_customer_pet_by_id(self, customer_id: int) -> Optional[Customer]:
        raise NotImplementedException()

    @abstractmethod
    def check_is_exists_customer_by_id(self, customer_id: int) -> bool:
        raise NotImplementedException()

    @abstractmethod
    def check_is_exists_customer_by_pet_kindergarden_id_and_phone_number(
        self, pet_kindergarden_id: int, phone_number: str
    ) -> bool:
        raise NotImplementedException()

    @abstractmethod
    def get_customer_queryset_by_pet_kindergarden_id(self, pet_kindergarden_id: int) -> QuerySet[Customer]:
        raise NotImplementedException()

    @abstractmethod
    def get_customer_by_id_and_customer_pet_id_for_reservation(
        self,
        customer_id: int,
        customer_pet_id: int,
    ) -> Optional[Customer]:
        raise NotImplementedException()


class AbstractCustomerTicketSelector(ABC):
    @abstractmethod
    def get_customer_ticket_with_ticket_queryset_by_customer_id(self, customer_id: int) -> QuerySet[CustomerTicket]:
        raise NotImplementedException()

    @abstractmethod
    def get_customer_ticket_list_by_customer_id_for_reservation(self, customer_id: int) -> dict[str, list]:
        raise NotImplementedException()

    @abstractmethod
    def get_customer_ticket_with_ticket_by_id(self, customer_ticket_id: int) -> Optional[CustomerTicket]:
        raise NotImplementedException()


class AbstractCustomerTicketReservationSelector(ABC):
    @abstractmethod
    def get_customer_ticket_reservation_list_by_customer_id(
        self, customer_id: int
    ) -> QuerySet[CustomerTicketReservation]:
        raise NotImplementedException()


class AbstractCustomerPetSelector(ABC):
    @abstractmethod
    def get_undeleted_customer_pet_queryset_by_names_and_customer_id(
        self, names: List[str], customer_id: int
    ) -> QuerySet[CustomerPet]:
        raise NotImplementedException()

    @abstractmethod
    def check_is_exists_undeleted_customer_pet_by_names_and_customer_id(
        self, names: List[str], customer_id: int
    ) -> bool:
        raise NotImplementedException()

    @abstractmethod
    def get_customer_pet_list_by_keyword_for_reservation(self, keyword: str) -> QuerySet[CustomerPet]:
        raise NotImplementedException()
