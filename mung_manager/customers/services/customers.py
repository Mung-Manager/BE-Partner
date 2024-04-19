import csv
from itertools import islice
from typing import List, Optional

from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db import transaction
from django.utils import timezone

from mung_manager.common.exception.exceptions import (
    AlreadyExistsException,
    NotFoundException,
    ValidationException,
)
from mung_manager.common.services import update_model
from mung_manager.common.validators import PhoneNumberValidator
from mung_manager.customers.models import Customer, CustomerPet
from mung_manager.customers.selectors.customers import CustomerSelector
from mung_manager.customers.services.abstracts import AbstractCustomerService
from mung_manager.pet_kindergardens.selectors.pet_kindergardens import (
    PetKindergardenSelector,
)


class CustomerService(AbstractCustomerService):
    """이 클래스는 고객을 데이터베이스에서 PUSH하는 비즈니스 로직을 담당합니다."""

    def __init__(self, customer_selector: CustomerSelector, pet_kindergarden_selector: PetKindergardenSelector):
        self._customer_selector = customer_selector
        self._pet_kindergarden_selector = pet_kindergarden_selector

    @transaction.atomic
    def create_customer(self, user, pet_kindergarden_id: int, name: str, phone_number: str, pets: List[str]) -> Customer:
        """이 함수는 고객을 검증 후 생성합니다.

        Args:
            user: 유저 객체
            pet_kindergarden_id (int): 반려동물 유치원 아이디
            name (str): 고객 이름
            phone_number (str): 고객 전화번호
            pets (List[str]): 반려동물 이름

        Returns:
            Customer: 고객 객체
        """
        # 반려동물 이름 중복 검사
        if len(pets) != len(set(pets)):
            raise ValidationException("Customer pet name is duplicated.")

        self._pet_kindergarden_selector.check_is_exists_pet_kindergarden_by_id_and_user(
            pet_kindergarten_id=pet_kindergarden_id,
            user=user,
        )

        self._customer_selector.check_is_exists_customer_by_pet_kindergarden_id_and_phone_number(
            pet_kindergarden_id=pet_kindergarden_id,
            phone_number=phone_number,
        )

        customer = Customer.objects.create(
            pet_kindergarden_id=pet_kindergarden_id,
            name=name,
            phone_number=phone_number,
        )

        pet_instances = [CustomerPet(name=pet, customer=customer) for pet in pets]

        CustomerPet.objects.bulk_create(pet_instances)

        return customer

    @transaction.atomic
    def create_customers_by_csv(self, user, pet_kindergarden_id: int, csv_file: InMemoryUploadedFile) -> List[Customer]:
        """
        이 함수는 CSV 파일을 읽어서 고객을 생성합니다.

        Args:
            user: 유저 객체
            pet_kindergarden_id (int): 반려동물 유치원 아이디
            csv_file (File): CSV 파일

        Returns:
            QuerySet[Customer]: 고객 객체
        """
        self._pet_kindergarden_selector.check_is_exists_pet_kindergarden_by_id_and_user(
            pet_kindergarten_id=pet_kindergarden_id,
            user=user,
        )

        # CSV 파일을 읽어서 데이터 추출
        decoded_file = csv_file.read().decode("utf-8").splitlines()
        reader = csv.reader(decoded_file)

        customer_instances: List[Customer] = []
        pet_instances: List[CustomerPet] = []

        # CSV 파일을 읽어서 고객 객체를 생성
        for idx, row in islice(enumerate(reader), 3, None):
            # csv 파일의 row가 비어있는지 검증
            if any(cell.strip() == "" for cell in row):
                raise ValidationException("Csv file row is empty.")

            # row 데이터 추출
            name, phone_number, pet_data = map(str.strip, row)

            # 전화번호 유효성 검사
            PhoneNumberValidator()(phone_number)

            # 반려동물 이름 중복 검사
            if len(pet_data.split(",")) != len(set(pet_data.split(","))):
                raise ValidationException("Customer pet name is duplicated.")

            # csv 파일에 동일한 전화번호가 존재하는지 검증
            if phone_number in [customer.phone_number for customer in customer_instances]:
                raise ValidationException("Csv file phone number is duplicated.")

            # 고객 인스턴스 생성
            customer = Customer(
                pet_kindergarden_id=pet_kindergarden_id,
                name=name,
                phone_number=phone_number,
            )
            customer_instances.append(customer)

            # 고객 반려동물 인스턴스 생성
            pets = [pet.strip() for pet in pet_data.split(",")]
            pet_instances.extend(CustomerPet(name=pet, customer=customer) for pet in pets)

        # csv 파일 닫기
        csv_file.close()

        # 전화번호로 기존 고객이 존재하는지 검증
        original_customer_phone_number_instances = self._customer_selector.get_customer_queryset_by_pet_kindergarden_id(
            pet_kindergarden_id=pet_kindergarden_id
        ).values_list("phone_number", flat=True)

        for customer_instance in customer_instances:
            if customer_instance.phone_number in original_customer_phone_number_instances:
                raise AlreadyExistsException(detail="Customer already exists.", code="already_exists_customer")

        # 최종 고객, 고객 반려동물 인스턴스 저장
        customers = Customer.objects.bulk_create(customer_instances)
        CustomerPet.objects.bulk_create(pet_instances)
        return customers

    @transaction.atomic
    def toggle_customer_is_active(self, user, customer_id: int, pet_kindergarden_id: int) -> Customer:
        """
        이 함수는 고객의 활성화/비활성화를 변경합니다.

        Args:
            user: 유저 객체
            customer_id (int): 고객 아이디
            pet_kindergarden_id (int): 반려동물 유치원 아이디

        Returns:
            Customer: 고객 객체
        """
        self._pet_kindergarden_selector.check_is_exists_pet_kindergarden_by_id_and_user(
            pet_kindergarten_id=pet_kindergarden_id,
            user=user,
        )

        # 고객이 존재하는지 검증
        customer = self._customer_selector.get_customer_by_id(customer_id=customer_id)
        if customer is None:
            raise NotFoundException(detail="Customer does not exist.", code="not_found_customer")

        # 고객 활성화/비활성화
        fields = ["is_active"]
        data = {"is_active": not customer.is_active}
        customer, has_updated = update_model(instance=customer, fields=fields, data=data)

        return customer

    @transaction.atomic
    def update_customer(
        self, user, pet_kindergarden_id: int, customer_id: int, name: str, phone_number: str, pets: List[str], memo: str
    ) -> Optional[Customer]:
        """
        이 함수는 고객 정보를 업데이트합니다.

        Args:
            user: 유저 객체
            customer_id (int): 고객 아이디
            name (str): 고객 이름
            phone_number (str): 고객 전화번호
            pets (List[str]): 반려동물 이름
            memo (str): 고객 메모

        Returns:
            Customer: 고객 객체
        """
        self._pet_kindergarden_selector.check_is_exists_pet_kindergarden_by_id_and_user(
            pet_kindergarten_id=pet_kindergarden_id,
            user=user,
        )

        # 반려동물 이름 중복 검사
        if len(pets) != len(set(pets)):
            raise ValidationException("Customer pet name is duplicated.")

        # 고객이 존재하는지 검증
        customer = self._customer_selector.get_customer_by_id(customer_id=customer_id)

        if customer is None:
            raise NotFoundException(detail="Customer does not exist.", code="not_found_customer")

        # 고객 정보 업데이트
        fields = ["name", "memo"]
        data = {"name": name, "memo": memo}

        # 유저와 연결되어 있지 않은 경우만 전화번호 업데이트
        if customer.user is None:
            fields.append("phone_number")
            data["phone_number"] = phone_number

        customer, has_updated = update_model(instance=customer, fields=fields, data=data)

        # @TODO: 예약, 등록이 있을 경우 예외처리
        # 고객 반려동물 삭제할 반려동물 조회
        customer_pets_to_be_deleted = customer.customer_pets.filter(is_deleted=False, deleted_at__isnull=True).exclude(name__in=pets)

        # 삭제할 반려동물이 존재하면 소프트 삭제
        if customer_pets_to_be_deleted.exists():
            customer_pets_to_be_deleted.update(is_deleted=True, deleted_at=timezone.now())

        customer_pet_names = customer.customer_pets.values_list("name", flat=True)

        customer_pets_to_be_created = [CustomerPet(name=pet, customer=customer) for pet in pets if pet not in customer_pet_names]

        # 반려동물 업데이트
        if customer_pets_to_be_created:
            customer.customer_pets.bulk_create(customer_pets_to_be_created)

        # 변경된 고객 정보 반환
        customer = self._customer_selector.get_customer_with_undeleted_customer_pet_by_id(customer_id=customer_id)
        return customer
