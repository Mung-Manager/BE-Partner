from django.db import transaction
from django.utils import timezone

from mung_manager.common.constants import SYSTEM_CODE
from mung_manager.common.selectors import (
    check_object_or_not_found,
    get_object_or_not_found,
)
from mung_manager.common.services import update_model
from mung_manager.pet_kindergardens.selectors.pet_kindergardens import (
    PetKindergardenSelector,
)
from mung_manager.tickets.models import Ticket
from mung_manager.tickets.selectors.tickets import TicketSelector
from mung_manager.tickets.services.abstracts import AbstractTicketService


class TicketService(AbstractTicketService):
    """이 클래스는 티켓을 데이터베이스에서 PUSH 또는 검증하는 역할을 담당합니다."""

    def __init__(
        self,
        ticket_selector: TicketSelector,
        pet_kindergarden_selector: PetKindergardenSelector,
    ):
        self._ticket_selector = ticket_selector
        self._pet_kindergarden_selector = pet_kindergarden_selector

    @transaction.atomic
    def create_ticket(
        self,
        pet_kindergarden_id: int,
        user,
        usage_time_count: int,
        usage_count: int,
        usage_period_in_days_count: int,
        price: int,
        ticket_type: str,
    ) -> Ticket:
        """이 함수는 티켓 데이터를 받아 티켓을 생성합니다.

        Args:
            pet_kindergarden_id: 반려동물 유치원 아이디입니다.
            usage_time_count: 사용시간 횟수입니다.
            usage_count: 사용횟수입니다.
            usage_period_in_days_count: 사용기간 횟수입니다.
            price: 가격입니다.
            ticket_type: 티켓 타입입니다.

        Returns:
            Ticket: 티켓 객체입니다.
        """
        check_object_or_not_found(
            self._pet_kindergarden_selector.check_is_exists_pet_kindergarden_by_id_and_user(
                pet_kindergarten_id=pet_kindergarden_id,
                user=user,
            ),
            msg=SYSTEM_CODE.message("NOT_FOUND_PET_KINDERGARDEN"),
            code=SYSTEM_CODE.code("NOT_FOUND_PET_KINDERGARDEN"),
        )
        ticket = Ticket.objects.create(
            pet_kindergarden_id=pet_kindergarden_id,
            usage_time_count=usage_time_count,
            usage_count=usage_count,
            usage_period_in_days_count=usage_period_in_days_count,
            price=price,
            ticket_type=ticket_type,
            deleted_at=None,
        )

        return ticket

    @transaction.atomic
    def delete_ticket(self, ticket_id: int, pet_kindergarden_id: int, user) -> Ticket:
        """이 함수는 티켓을 검증 후 삭제 여부를 True로 변경합니다.

        Args:
            ticket_id: 티켓 아이디입니다.
            pet_kindergarden_id: 반려동물 유치원 아이디입니다.
            user: 유저 객체입니다.

        Returns:
            Ticket: 티켓 객체입니다.
        """
        check_object_or_not_found(
            self._pet_kindergarden_selector.check_is_exists_pet_kindergarden_by_id_and_user(
                pet_kindergarten_id=pet_kindergarden_id,
                user=user,
            ),
            msg=SYSTEM_CODE.message("NOT_FOUND_PET_KINDERGARDEN"),
            code=SYSTEM_CODE.code("NOT_FOUND_PET_KINDERGARDEN"),
        )
        ticket = get_object_or_not_found(
            self._ticket_selector.get_ticket_by_id(ticket_id=ticket_id),
            msg=SYSTEM_CODE.message("NOT_FOUND_TICKET"),
            code=SYSTEM_CODE.code("NOT_FOUND_TICKET"),
        )
        if ticket.is_deleted is False and ticket.deleted_at is None:
            fields = ["is_deleted", "deleted_at"]
            data = {"is_deleted": True, "deleted_at": timezone.now()}
            ticket, has_updated = update_model(
                instance=ticket, fields=fields, data=data
            )
        return ticket
