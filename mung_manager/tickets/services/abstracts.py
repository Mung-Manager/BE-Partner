from abc import ABC, abstractmethod

from mung_manager.tickets.models import Ticket


class AbstractTicketService(ABC):
    @abstractmethod
    def create_ticket(
        self,
        pet_kindergarden_id: int,
        user,
        usage_time: int,
        usage_count: int,
        usage_period_in_days_count: int,
        price: int,
        ticket_type: str,
    ) -> Ticket:
        pass

    @abstractmethod
    def delete_ticket(self, ticket_id: int, pet_kindergarden_id: int, user) -> Ticket:
        pass
