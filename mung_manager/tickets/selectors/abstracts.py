from abc import ABC, abstractmethod
from typing import Optional

from django.db.models.query import QuerySet

from mung_manager.tickets.models import Ticket


class AbstractTicketSelector(ABC):
    @abstractmethod
    def get_ticket_by_id(self, ticket_id: int) -> Optional[Ticket]:
        pass

    @abstractmethod
    def get_ticket_queryset_by_pet_kindergarden_id(
        self, pet_kindergarden_id: int
    ) -> QuerySet[Ticket]:
        pass

    @abstractmethod
    def get_undeleted_ticket_by_pet_kindergarden_id(
        self, pet_kindergarden_id: int
    ) -> QuerySet[Ticket]:
        pass

    @abstractmethod
    def get_undeleted_ticket_by_id(self, ticket_id: int) -> Optional[Ticket]:
        pass
