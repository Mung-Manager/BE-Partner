# from django.db import transaction
# from mung_manager.customers.selectors.customers import CustomerSelector
# from mung_manager.customers.services.abstracts import AbstractCustomerPetService
# from mung_manager.pet_kindergardens.selectors.pet_kindergardens import (
#     PetKindergardenSelector,
# )


# class CustomerPetService(AbstractCustomerPetService):
#     """이 클래스는 고객 반려동물을 데이터베이스에서 PUSH하는 비즈니스 로직을 담당합니다."""

#     def __init__(
#         self,
#         customer_selector: CustomerSelector,
#         pet_kindergarden_selector: PetKindergardenSelector,
#     ):
#         self._customer_selector = customer_selector
#         self._pet_kindergarden_selector = pet_kindergarden_selector

#     @transaction.atomic
#     def check_is_possible_delete_customer_pet(self, user, pet_kindergarden_id: int, customer_id: int, pet_id: int) -> bool:
#         """이 함수는 고객의 반려동물 삭제가 가능한지 확인합니다.

#         Args:
#             user: 유저 객체
#             pet_kindergarden_id (int): 반려동물 유치원 아이디
#             customer_id (int): 고객 아이디
#             pet_id (int): 반려동물 아이디

#         Returns:
#             bool: 반려동물 삭제 가능 여부
#         """
#         self._pet_kindergarden_selector.check_is_exists_pet_kindergarden_by_id_and_user(
#             pet_kindergarten_id=pet_kindergarden_id,
#             user=user,
#         )
#         pass
