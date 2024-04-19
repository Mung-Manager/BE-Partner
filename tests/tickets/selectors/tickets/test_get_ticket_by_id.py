import pytest

from mung_manager.tickets.selectors.tickets import TicketSelector

pytestmark = pytest.mark.django_db


class TestTicketById:
    """
    TicketSelector의 get_ticket_by_id 테스트 클래스

    - Test List:
        Success:
            - get_ticket_by_id_success
        Fail:
            - get_ticket_by_id_fail_does_not_exist
    """

    def setup_method(self):
        self.ticket_selector = TicketSelector()

    def test_get_ticket_by_id_success(self, ticket):
        """티켓 아이디로 티켓 조회 성공 테스트

        Args:
            ticket : 티켓
        """
        ticket_data = self.ticket_selector.get_ticket_by_id(ticket.id)

        assert ticket_data == ticket

    def test_get_ticket_by_id_fail_does_not_exist(self):
        """티켓 아이디로 티켓 조회 실패 테스트

        티켓이 존재하지 않는 경우
        """
        ticket_data = self.ticket_selector.get_ticket_by_id(999)

        assert ticket_data is None
