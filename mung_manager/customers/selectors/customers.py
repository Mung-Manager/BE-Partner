from typing import Optional

from django.db.models import Max, Prefetch
from django.db.models.functions import Greatest
from django.db.models.query import QuerySet

from mung_manager.customers.filters import CustomerFilter
from mung_manager.customers.models import Customer, CustomerPet
from mung_manager.customers.selectors.abstracts import AbstractCustomerSelector


class CustomerSelector(AbstractCustomerSelector):
    """이 클래스는 고객을 데이터베이스에서 PULL하는 비즈니스 로직을 담당합니다."""

    def get_customer_list(self, filters: Optional[dict] = None) -> QuerySet[Customer]:
        """이 함수는 필터로 삭제되지 않은 고객 반려동물, 최근 예약, 고객 티켓, 티켓을 포함한 고객 리스트를 가져옵니다.

        Args:
            filters (Optional[dict]): 필터

        Returns:
            QuerySet[Customer]: 고객 리스트 쿼리셋이며 존재하지 않으면 빈 쿼리셋을 반환
        """
        filters = filters or {}
        qs = (
            Customer.objects.all()
            .prefetch_related("customer_tickets", "customer_tickets__ticket")
            .prefetch_related(
                Prefetch(
                    "customer_pets",
                    queryset=CustomerPet.objects.filter(is_deleted=False, deleted_at__isnull=True),
                    to_attr="undeleted_customer_pets",
                )
            )
            .annotate(
                recent_reserved_at=Greatest(
                    Max("reservations__reserved_at"),
                    Max("reservations__updated_reserved_at"),
                ),
            )
        )

        return CustomerFilter(filters, qs).qs

    def get_customer_by_id(self, customer_id: int) -> Optional[Customer]:
        """이 함수는 고객 아이디로 고객을 가져옵니다.

        Args:
            customer_id (int): 고객 아이디

        Returns:
            Optional[Customer]: 고객 객체이며 존재하지 않으면 None을 반환
        """
        try:
            return Customer.objects.filter(id=customer_id).get()
        except Customer.DoesNotExist:
            return None

    def get_customer_with_undeleted_customer_pet_by_id(self, customer_id: int) -> Optional[Customer]:
        """이 함수는 고객 아이디로 고객과 삭제되지 않은 고객 반려동물을 가져옵니다.

        Args:
            customer_id (int): 고객 아이디

        Returns:
            Optional[Customer]: 고객 객체이며 존재하지 않으면 None을 반환
        """
        try:
            return (
                Customer.objects.prefetch_related(
                    Prefetch(
                        "customer_pets",
                        queryset=CustomerPet.objects.filter(is_deleted=False, deleted_at__isnull=True),
                        to_attr="undeleted_customer_pets",
                    )
                )
                .filter(id=customer_id)
                .get()
            )
        except Customer.DoesNotExist:
            return None

    def check_is_exists_customer_by_id(self, customer_id: int) -> bool:
        """이 함수는 고객 아이디로 고객이 존재하는지 확인합니다.

        Args:
            customer_id (int): 고객 아이디

        Returns:
            bool: 고객이 존재하면 True를 반환하며 존재하지 않으면 False를 반환
        """
        return Customer.objects.filter(id=customer_id).exists()

    def check_is_exists_customer_by_pet_kindergarden_id_and_phone_number(
        self, pet_kindergarden_id: int, phone_number: str
    ) -> bool:
        """이 함수는 반려동물 유치원 아이디와 전화번호로 고객이 존재하는지 확인합니다.

        Args:
            pet_kindergarden_id (int): 반려동물 유치원 아이디
            phone_number (str): 고객 전화번호

        Returns:
            bool: 고객이 존재하면 True를 반환하며 존재하지 않으면 False를 반환
        """
        return Customer.objects.filter(pet_kindergarden_id=pet_kindergarden_id, phone_number=phone_number).exists()

    def get_customer_queryset_by_pet_kindergarden_id(self, pet_kindergarden_id: int) -> QuerySet[Customer]:
        """이 함수는 반려동물 유치원 아이디로 고객을 조회합니다.

        Args:
            pet_kindergarden_id (int): 반려동물 유치원 아이디

        Returns:
            QuerySet[Customer]: 고객 리스트 쿼리셋이며 존재하지 않으면 빈 쿼리셋을 반환
        """
        return Customer.objects.filter(pet_kindergarden_id=pet_kindergarden_id)
