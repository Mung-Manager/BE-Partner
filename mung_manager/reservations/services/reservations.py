from concurrency.exceptions import RecordModifiedError
from django.db import transaction

from mung_manager.common.constants import SYSTEM_CODE
from mung_manager.common.selectors import (
    check_object_or_already_exist,
    check_object_or_not_found,
    get_object_or_not_found,
)
from mung_manager.common.services import update_model
from mung_manager.customers.selectors.customer_tickets import CustomerTicketSelector
from mung_manager.customers.selectors.customers import CustomerSelector
from mung_manager.errors.exceptions import ValidationException
from mung_manager.pet_kindergardens.selectors.pet_kindergardens import (
    PetKindergardenSelector,
)
from mung_manager.reservations.enums import ReservationStatus
from mung_manager.reservations.models import Reservation
from mung_manager.reservations.selectors.reservations import ReservationSelector
from mung_manager.reservations.services.abstracts import AbstractReservationService


class ReservationService(AbstractReservationService):
    """이 클래스는 예약을 DB에 PUSH하는 비즈니스 로직을 담당합니다."""

    def __init__(
        self,
        pet_kindergarden_selector: PetKindergardenSelector,
        customer_selector: CustomerSelector,
        customer_ticket_selector: CustomerTicketSelector,
        reservation_selector: ReservationSelector,
    ):
        self._pet_kindergarden_selector = pet_kindergarden_selector
        self._customer_selector = customer_selector
        self._customer_ticket_selector = customer_ticket_selector
        self._reservation_selector = reservation_selector

    @transaction.atomic
    def toggle_reservation_is_attended(self, pet_kindergarden_id: int, reservation_id: int, user) -> Reservation:
        """이 함수는 예약의 출석 활성화/비활성화를 변경합니다.

        Args:
            pet_kindergarden_id (int): 반려동물 유치원 아이디
            reservation_id (int): 예약 아이디
            user: 유저 객체

        Returns:
            Reservation: 예약 객체
        """
        check_object_or_not_found(
            self._pet_kindergarden_selector.check_is_exists_pet_kindergarden_by_id_and_user(
                pet_kindergarden_id=pet_kindergarden_id,
                user=user,
            ),
            msg=SYSTEM_CODE.message("NOT_FOUND_PET_KINDERGARDEN"),
            code=SYSTEM_CODE.code("NOT_FOUND_PET_KINDERGARDEN"),
        )

        reservation = get_object_or_not_found(
            self._reservation_selector.get_reservation_by_id(
                reservation_id=reservation_id,
            ),
            msg=SYSTEM_CODE.message("NOT_FOUND_RESERVATION"),
            code=SYSTEM_CODE.code("NOT_FOUND_RESERVATION"),
        )

        data = {
            "is_attended": not reservation.is_attended,
        }
        reservation, has_updated = update_model(
            instance=reservation,
            data=data,
            fields=list(data.keys()),
        )
        return reservation

    @transaction.atomic
    def create_reservation(
        self,
        pet_kindergarden_id: int,
        customer_ticket_id: int,
        customer_id: int,
        customer_pet_id: int,
        reserved_at: str,
        end_at: str,
        user,
    ) -> Reservation:
        """이 함수는 예약을 생성합니다.

        Args:
            pet_kindergarden_id (int): 반려동물 유치원 아이디
            customer_ticket_id (int): 고객 티켓 아이디
            customer_id (int): 고객 아이디
            customer_pet_id (int): 고객 반려동물 아이디
            reserved_at (str): 예약 시작 시간
            end_at (str): 예약 종료 시간
            user: 유저 객체

        Returns:
            Reservation: 예약 객체
        """
        # 유저 반려동물 유치원 검증
        check_object_or_not_found(
            self._pet_kindergarden_selector.check_is_exists_pet_kindergarden_by_id_and_user(
                pet_kindergarden_id=pet_kindergarden_id,
                user=user,
            ),
            msg=SYSTEM_CODE.message("NOT_FOUND_PET_KINDERGARDEN"),
            code=SYSTEM_CODE.code("NOT_FOUND_PET_KINDERGARDEN"),
        )
        # 고객 및 고객 반려동물 검증
        check_object_or_not_found(
            self._customer_selector.get_customer_by_id_and_customer_pet_id_for_reservation(
                customer_id=customer_id,
                customer_pet_id=customer_pet_id,
            ),
            msg=SYSTEM_CODE.message("NOT_FOUND_CUSTOMER"),
            code=SYSTEM_CODE.code("NOT_FOUND_CUSTOMER"),
        )
        # 반려동물 동일 시간 예약 검증
        check_object_or_already_exist(
            self._reservation_selector.check_is_exists_reservation_by_customer_pet_id_and_reserved_at(
                customer_pet_id=customer_pet_id,
                reserved_at=reserved_at,
            ),
            msg=SYSTEM_CODE.message("ALREADY_EXISTS_RESERVATION_CUSTOMER_PET"),
            code=SYSTEM_CODE.code("ALREADY_EXISTS_RESERVATION_CUSTOMER_PET"),
        )
        # 티켓 존재 여부 검증
        customer_ticket = get_object_or_not_found(
            self._customer_ticket_selector.get_customer_ticket_with_ticket_by_id(customer_ticket_id),
            msg=SYSTEM_CODE.message("NOT_FOUND_CUSTOMER_TICKET"),
            code=SYSTEM_CODE.code("NOT_FOUND_CUSTOMER_TICKET"),
        )
        # 티켓에 대한 시간 검증 (reserved_at ~ end_at)
        # 종일은 00:00 ~ 23:59:59까지 사용 가능

        # if customer_ticket.ticket.ticket_type == TicketType.ALL_DAY.value:
        #     # reserved_at이 동일날짜의 00:00 end_at이 동일날짜의 23:59:59인지 검증 아닐 경우 예외 발생
        #     if not (reserved_at == reserved_at.split("T")[0] +
        # "T00:00:00" and end_at == end_at.split("T")[0] + "T23:59:59"):
        #         raise ValidationException(
        #             detail=SYSTEM_CODE.message("INVALID_RESERVED_AT"),
        #             code=SYSTEM_CODE.code("INVALID_RESERVED_AT"),
        #         )
        # # 시간은 이용권의 usage_time만큼 사용 가능
        # if customer_ticket.ticket.ticket_type == TicketType.TIME.value:
        #     # reserved_at ~ end_at 시간이 이용권의 usage_time보다 큰지 검증 아닐 경우 예외 발생
        #     if duration < customer_ticket.ticket.usage_time:
        #         raise ValidationException(
        #             detail=SYSTEM_CODE.message("INVALID_END_AT"),
        #             code=SYSTEM_CODE.code("INVALID_END_AT"),
        #         )
        # # 호텔은 이용권의 usage_period만큼 사용 가능
        # if customer_ticket.ticket.ticket_type == TicketType.HOTEL.value:
        #     # reserved_at ~ end_at 시간이 이용권의 usage_period보다 큰지 검증 아닐 경우 예외 발생
        #     if not (end_at - reserved_at) >= customer_ticket.ticket.usage_period:
        #         raise ValidationException(
        #             detail=SYSTEM_CODE.message("INVALID_END_AT"),
        #             code=SYSTEM_CODE.code("INVALID_END_AT"),
        #         )

        # 티켓 사용 횟수가 남아있는지 검증
        if customer_ticket.unused_count <= 0:
            raise ValidationException(
                detail=SYSTEM_CODE.message("NO_CUSTOMER_TICKET_COUNT"),
                code=SYSTEM_CODE.code("NO_CUSTOMER_TICKET_COUNT"),
            )

        # 티켓 횟수 증감 처리(낙관적 잠금 처리)
        try:
            customer_ticket.used_count += 1
            customer_ticket.unused_count -= 1
            customer_ticket.save(update_fields=["used_count", "unused_count", "version"])

        except RecordModifiedError:
            raise ValidationException(
                detail=SYSTEM_CODE.message("CONFILCT_CUSTOMER_TICKET"),
                code=SYSTEM_CODE.code("CONFILCT_CUSTOMER_TICKET"),
            )

        # 예약 생성
        reservation = Reservation.objects.create(
            reserved_at=reserved_at,
            end_at=end_at,
            is_attended=False,
            reservation_status=ReservationStatus.PENDING.value,
            pet_kindergarden_id=pet_kindergarden_id,
            customer_id=customer_id,
            customer_pet_id=customer_pet_id,
            customer_ticket_id=customer_ticket_id,
        )
        return reservation
