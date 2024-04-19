from abc import ABC, abstractmethod
from typing import Optional

from django.db.models.query import QuerySet

from mung_manager.customers.models import Customer, CustomerTicket, CustomerTicketLog


class AbstractCustomerSelector(ABC):
    @abstractmethod
    def get_customer_list(self, filters: Optional[dict] = None) -> QuerySet[Customer]:
        pass

    @abstractmethod
    def get_customer_by_id(self, customer_id: int) -> Optional[Customer]:
        pass

    @abstractmethod
    def get_customer_with_undeleted_customer_pet_by_id(self, customer_id: int) -> Optional[Customer]:
        pass

    @abstractmethod
    def check_is_exists_customer_by_id(self, customer_id: int) -> bool:
        pass

    @abstractmethod
    def check_is_exists_customer_by_pet_kindergarden_id_and_phone_number(self, pet_kindergarten_id: int, phone_number: str) -> bool:
        pass

    @abstractmethod
    def get_customer_queryset_by_pet_kindergarden_id(self, pet_kindergarten_id: int) -> QuerySet[Customer]:
        pass


class AbstractCustomerTicketSelector(ABC):
    @abstractmethod
    def get_customer_ticket_with_ticket_queryset_by_customer_id(self, customer_id: int) -> QuerySet[CustomerTicket]:
        pass


class AbstractCustomerTicketLogSelector(ABC):
    @abstractmethod
    def get_customer_ticket_log_with_customer_ticket_and_ticket_queryset_by_customer_id_order_by_created_at_desc(
        self, customer_id: int
    ) -> QuerySet[CustomerTicketLog]:
        pass


class AbstractCustomerPetSelector(ABC):
    @abstractmethod
    def check_is_exists_customer_pet_by_id_and_customer_id(self, pet_id: int, customer_id: int) -> bool:
        pass
