import pytest

from mung_manager.tickets.enums import TicketType
from mung_manager.tickets.services.tickets import TicketService

pytestmark = pytest.mark.django_db


class TestCreateTicket:
    """
    TicketService의 create_ticket 테스트 클래스

    - Test List:
        Success:
            - create_ticket_success
    """

    def setup_method(self):
        self.ticket_service = TicketService()

    def test_create_ticket_success(self, pet_kindergarden):
        """티켓 생성 성공 테스트

        Args:
            pet_kindergarden : 반려동물 유치원
        """
        ticket_data = {
            "pet_kindergarden_id": pet_kindergarden.id,
            "usage_time_count": 10,
            "usage_count": 10,
            "usage_period_in_days_count": 10,
            "ticket_type": TicketType.TIME.value,
            "price": 100000,
        }
        ticket = self.ticket_service.create_ticket(
            pet_kindergarden_id=ticket_data["pet_kindergarden_id"],
            ticket_type=ticket_data["ticket_type"],
            price=ticket_data["price"],
            usage_time_count=ticket_data["usage_time_count"],
            usage_period_in_days_count=ticket_data["usage_period_in_days_count"],
            usage_count=ticket_data["usage_count"],
        )

        assert ticket.pet_kindergarden_id == ticket_data["pet_kindergarden_id"]
        assert ticket.usage_time_count == ticket_data["usage_time_count"]
        assert ticket.usage_count == ticket_data["usage_count"]
        assert ticket.usage_period_in_days_count == ticket_data["usage_period_in_days_count"]
        assert ticket.price == ticket_data["price"]
        assert ticket.ticket_type == ticket_data["ticket_type"]
