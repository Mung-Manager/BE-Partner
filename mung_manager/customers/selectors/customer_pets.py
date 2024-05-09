from typing import List

from django.db.models.query import QuerySet

from mung_manager.customers.models import CustomerPet
from mung_manager.customers.selectors.abstracts import AbstractCustomerPetSelector


class CustomerPetSelector(AbstractCustomerPetSelector):
    """이 클래스는 고객 반려동물을 데이터베이스에서 PULL하는 비즈니스 로직을 담당합니다."""

    def get_undeleted_customer_pet_queryset_by_names_and_customer_id(
        self, names: List[str], customer_id: int
    ) -> QuerySet[CustomerPet]:
        """고객 반려동물 아이디로 삭제되지 않은 고객 반려동물을 가져옵니다.

        Args:
            customer_pet_id (int): 고객 반려동물 아이디

        Returns:
            CustomerPet: 삭제되지 않은 고객 반려동물
        """
        return CustomerPet.objects.filter(
            name__in=names,
            customer_id=customer_id,
            is_deleted=False,
            deleted_at__isnull=True,
        )

    def check_is_exists_undeleted_customer_pet_by_names_and_customer_id(
        self, names: List[str], customer_id: int
    ) -> bool:
        """반려동물 이름들과 고객 아이디로 삭제되지 않은 고객 반려동물이 존재하는지 확인합니다.

        Args:
            names (List[str]): 반려동물 이름 리스트
            customer_id (int): 고객 아이디

        Returns:
            bool: 고객 반려동물이 존재하면 True, 아니면 False를 반환
        """
        return CustomerPet.objects.filter(
            name__in=names,
            customer_id=customer_id,
            is_deleted=False,
            deleted_at__isnull=True,
        ).exists()
