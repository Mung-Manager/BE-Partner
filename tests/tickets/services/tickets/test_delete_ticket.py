import pytest

from mung_manager.common.exception.exceptions import NotFoundException
from mung_manager.tickets.services.tickets import TicketService

pytestmark = pytest.mark.django_db


class TestDeleteTicket:
    """
    TicketService의 delete_ticket 테스트 클래스

    - Test List:
        Success:
            - delete_ticket_success
        Fail:
            - delete_ticket_fail_ticket_does_not_exist
            - delete_ticket_fail_pet_kindergarden_does_not_exist

    """

    def setup_method(self):
        self.ticket_service = TicketService()

    def test_delete_ticket_success(self, ticket):
        """티켓 삭제 성공 테스트

        Args:
            ticket : 티켓
        """
        ticket = self.ticket_service.delete_ticket(
            ticket_id=ticket.id,
            user=ticket.pet_kindergarden.user,
            pet_kindergarden_id=ticket.pet_kindergarden_id,
        )

        assert ticket.deleted_at is not None
        assert ticket.is_deleted is True

    def test_delete_ticket_fail_ticket_does_not_exist(self, pet_kindergarden):
        """티켓 삭제 실패 테스트 (존재하지 않는 티켓)

        Args:
            pet_kindergarden : 반려동물 유치원
        """

        with pytest.raises(NotFoundException) as e:
            self.ticket_service.delete_ticket(
                ticket_id=999,
                user=pet_kindergarden.user,
                pet_kindergarden_id=pet_kindergarden.id,
            )

        assert str(e.value) == "Ticket does not exist."
        assert isinstance(e.value, NotFoundException)

    def test_delete_ticket_fail_pet_kindergarden_does_not_exist(self, ticket):
        """티켓 삭제 실패 테스트 (존재하지 않는 반려동물 유치원)

        Args:
            ticket : 티켓
        """

        with pytest.raises(NotFoundException) as e:
            self.ticket_service.delete_ticket(
                ticket_id=ticket.id,
                user=ticket.pet_kindergarden.user,
                pet_kindergarden_id=999,
            )

        assert str(e.value) == "PetKindergarden does not exist."
        assert isinstance(e.value, NotFoundException)
