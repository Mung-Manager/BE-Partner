from datetime import timedelta

from django.db import transaction
from django.utils import timezone

from mung_manager.common.exception.exceptions import NotFoundException
from mung_manager.customers.models import CustomerTicket
from mung_manager.customers.selectors.customers import CustomerSelector
from mung_manager.customers.services.abstracts import AbstractCustomerTicketService
from mung_manager.pet_kindergardens.selectors.pet_kindergardens import (
    PetKindergardenSelector,
)
from mung_manager.tickets.selectors.tickets import TicketSelector


class CustomerTicketService(AbstractCustomerTicketService):
    """이 클래스는 고객의 티켓을 데이터베이스에서 PUSH하는 비즈니스 로직을 담당합니다."""

    def __init__(
        self, customer_selector: CustomerSelector, pet_kindergarden_selector: PetKindergardenSelector, ticket_selector: TicketSelector
    ):
        self._customer_selector = customer_selector
        self._pet_kindergarden_selector = pet_kindergarden_selector
        self._ticket_selector = ticket_selector

    @transaction.atomic
    def register_ticket(self, user, customer_id: int, pet_kindergarden_id: int, ticket_id: int) -> CustomerTicket:
        """이 함수는 고객의 티켓을 검증 후 등록합니다.

        Args:
            user: 유저 객체
            customer_id (int): 고객 아이디
            pet_kindergarden_id (int): 반려동물 유치원 아이디
            ticket_id (int): 티켓 아이디

        Returns:
            CustomerTicket: 고객의 티켓 객체
        """
        self._pet_kindergarden_selector.check_is_exists_pet_kindergarden_by_id_and_user(
            pet_kindergarten_id=pet_kindergarden_id,
            user=user,
        )

        self._customer_selector.check_is_exists_customer_by_id(customer_id)

        ticket = self._ticket_selector.get_undeleted_ticket_by_id(ticket_id)

        if ticket is None:
            raise NotFoundException(detail="Ticket does not exist.", code="not_found_ticket")

        customer_ticket = CustomerTicket.objects.create(
            customer_id=customer_id,
            ticket_id=ticket_id,
            expired_at=timezone.now() + timedelta(days=ticket.usage_period_in_days_count),
            total_count=ticket.usage_count,
            used_count=0,
        )

        return customer_ticket
