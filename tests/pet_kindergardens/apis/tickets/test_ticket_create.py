import pytest
from django.urls import reverse

from mung_manager.tickets.enums import TicketType
from tests.utils import IsAuthenticateTestCase

pytestmark = pytest.mark.django_db


class TestTicketCreateAPI(IsAuthenticateTestCase):
    """
    TicketCreateAPI 테스트 클래스

    - Test List:
        Success:
            - ticket_create_success
        Fail:
            - ticket_create_fail_not_authenticated
            - ticket_create_fail_permission_denied
            - ticket_create_fail_pet_kindergarden_does_not_exist
            - ticket_create_fail_ticket_type_invalid_choice
    """

    def test_ticket_create_success(self, pet_kindergarden):
        """티켓 생성 성공 테스트

        Args:
            pet_kindergarden : 반려동물 유치원
        """
        access_token = self.obtain_token(pet_kindergarden.user)
        self.authenticate_with_token(access_token)

        ticket_data = {
            "ticket_type": TicketType.TIME.value,
            "usage_time_count": 10,
            "usage_count": 10,
            "usage_period_in_days_count": 10,
            "price": 10000,
        }

        response = self.client.post(
            reverse("api-pet-kindergardens:pet-kindergarden-tickets-list", kwargs={"pet_kindergarden_id": pet_kindergarden.id}),
            data=ticket_data,
            format="json",
        )
        assert response.status_code == 201
        assert response.data["data"]["ticket_type"] == TicketType.TIME.value
        assert response.data["data"]["usage_time_count"] == ticket_data["usage_time_count"]
        assert response.data["data"]["usage_count"] == ticket_data["usage_count"]
        assert response.data["data"]["usage_period_in_days_count"] == ticket_data["usage_period_in_days_count"]
        assert response.data["data"]["price"] == ticket_data["price"]
        assert not response.data["data"]["is_deleted"]

    def test_ticket_create_fail_not_authenticated(self, pet_kindergarden):
        """티켓 생성 실패 테스트 (인증되지 않은 경우)

        Args:
            pet_kindergarden : 반려동물 유치원
        """
        response = self.client.post(
            reverse("api-pet-kindergardens:pet-kindergarden-tickets-list", kwargs={"pet_kindergarden_id": pet_kindergarden.id}),
            data={},
            format="json",
        )
        assert response.status_code == 401
        assert response.data["code"] == "not_authenticated"
        assert response.data["message"] == "Authentication credentials were not provided."

    def test_ticket_create_fail_permission_denied(self, pet_kindergarden, active_guest_user):
        """티켓 생성 실패 테스트 (권한이 없는 경우)

        Args:
            pet_kindergarden : 반려동물 유치원
            active_guest_user : 활성화된 게스트 유저
        """
        access_token = self.obtain_token(active_guest_user)
        self.authenticate_with_token(access_token)

        response = self.client.get(
            reverse("api-pet-kindergardens:pet-kindergarden-tickets-list", kwargs={"pet_kindergarden_id": pet_kindergarden.id}),
        )
        assert response.status_code == 403
        assert response.data["code"] == "permission_denied"
        assert response.data["message"] == "You do not have permission to perform this action."

    def test_ticket_create_fail_pet_kindergarden_does_not_exist(self, active_partner_user):
        """티켓 생성 실패 테스트 (존재하지 않는 유치원)

        Args:
            active_partner_user : 활성화된 파트너 유저
        """
        access_token = self.obtain_token(active_partner_user)
        self.authenticate_with_token(access_token)

        ticket_data = {
            "ticket_type": TicketType.TIME.value,
            "usage_time_count": 10,
            "usage_count": 10,
            "usage_period_in_days_count": 10,
            "price": 10000,
        }

        response = self.client.post(
            reverse("api-pet-kindergardens:pet-kindergarden-tickets-list", kwargs={"pet_kindergarden_id": 1}),
            data=ticket_data,
            format="json",
        )
        assert response.status_code == 404
        assert response.data["code"] == "not_found_pet_kindergarden"
        assert response.data["message"] == "PetKindergarden does not exist."

    def test_ticket_create_fail_ticket_type_invalid_choice(self, pet_kindergarden):
        """티켓 생성 (티켓 타입이 선택지가 아닌 경우)

        Args:
            pet_kindergarden : 반려동물 유치원
        """
        access_token = self.obtain_token(pet_kindergarden.user)
        self.authenticate_with_token(access_token)

        ticket_data = {
            "ticket_type": "invalid_choice",
            "usage_time_count": 10,
            "usage_count": 10,
            "usage_period_in_days_count": 10,
            "price": 10000,
        }

        response = self.client.post(
            reverse("api-pet-kindergardens:pet-kindergarden-tickets-list", kwargs={"pet_kindergarden_id": pet_kindergarden.id}),
            data=ticket_data,
            format="json",
        )
        assert response.status_code == 400
        assert response.data["code"] == "invalid_parameter_format"
        assert response.data["message"] == {"ticket_type": ['"invalid_choice" is not a valid choice.']}
