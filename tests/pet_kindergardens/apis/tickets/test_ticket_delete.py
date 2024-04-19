import pytest
from django.urls import reverse

from tests.utils import IsAuthenticateTestCase

pytestmark = pytest.mark.django_db


class TestTicketDeleteAPI(IsAuthenticateTestCase):
    """
    TicketDeleteAPI 테스트 클래스

     - Test List:
         Success:
             - ticket_delete_success
         Fail:
             - ticket_delete_fail_not_authenticated
             - ticket_delete_fail_permission_denied
    """

    def test_ticket_delete_success(self, ticket):
        """티켓 삭제 성공 테스트

        Args:
            ticket : 티켓
        """
        access_token = self.obtain_token(ticket.pet_kindergarden.user)
        self.authenticate_with_token(access_token)

        response = self.client.delete(
            reverse(
                "api-pet-kindergardens:pet-kindergarden-tickets-detail",
                kwargs={"pet_kindergarden_id": ticket.pet_kindergarden.id, "ticket_id": ticket.id},
            ),
        )
        assert response.status_code == 204

    def test_ticket_delete_fail_not_authenticated(self, ticket):
        """티켓 삭제 실패 테스트 (인증되지 않은 경우)

        Args:
            pet_kindergarden : 반려동물 유치원
        """
        response = self.client.delete(
            reverse(
                "api-pet-kindergardens:pet-kindergarden-tickets-detail",
                kwargs={"pet_kindergarden_id": ticket.pet_kindergarden.id, "ticket_id": ticket.id},
            ),
        )
        assert response.status_code == 401
        assert response.data["code"] == "not_authenticated"
        assert response.data["message"] == "Authentication credentials were not provided."

    def test_ticket_delete_fail_permission_denied(self, ticket, active_guest_user):
        """티켓 삭제 실패 테스트 (권한이 없는 경우)

        Args:
            pet_kindergarden : 반려동물 유치원
            active_user : 활성화된 유저
        """
        access_token = self.obtain_token(active_guest_user)
        self.authenticate_with_token(access_token)

        response = self.client.delete(
            reverse(
                "api-pet-kindergardens:pet-kindergarden-tickets-detail",
                kwargs={"pet_kindergarden_id": ticket.pet_kindergarden.id, "ticket_id": ticket.id},
            ),
        )
        assert response.status_code == 403
        assert response.data["code"] == "permission_denied"
        assert response.data["message"] == "You do not have permission to perform this action."
