from mung_manager.customers.models import CustomerPet
from mung_manager.customers.selectors.abstracts import AbstractCustomerPetSelector


class CustomerPetSelector(AbstractCustomerPetSelector):
    """이 클래스는 고객 반려동물을 데이터베이스에서 PULL하는 비즈니스 로직을 담당합니다."""

    def check_is_exists_customer_pet_by_id_and_customer_id(self, pet_id: int, customer_id: int) -> bool:
        """이 함수는 반려동물 아이디와 고객 아이디로 반려동물이 존재하는지 확인합니다.

        Args:
            pet_id (int): 반려동물 아이디
            customer_id (int): 고객 아이디

        Returns:
            bool: 반려동물이 존재하면 True, 존재하지 않으면 False
        """
        return CustomerPet.objects.filter(id=pet_id, customer_id=customer_id).exists()
