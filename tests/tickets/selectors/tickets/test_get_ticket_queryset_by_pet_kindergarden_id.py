import pytest

from mung_manager.tickets.selectors.tickets import TicketSelector

pytestmark = pytest.mark.django_db


class TestGetTicketQuerysetByPetKindergardenId:
    """
    TicketSelector의 get_ticket_queryset_by_pet_kindergarden_id 테스트 클래스

    - Test List:
        Success:
            - get_ticket_queryset_by_pet_kindergarden_id_success
    """

    def setup_method(self):
        self.ticket_selector = TicketSelector()

    def test_get_ticket_queryset_by_pet_kindergarden_id_success(self, ticket):
        """반려동물 유치원 아이디로 티켓 쿼리셋 조회 성공 테스트

        Args:
            ticket : 티켓
        """
        ticket_queryset = self.ticket_selector.get_ticket_queryset_by_pet_kindergarden_id(ticket.pet_kindergarden_id)

        assert ticket_queryset[0] == ticket
