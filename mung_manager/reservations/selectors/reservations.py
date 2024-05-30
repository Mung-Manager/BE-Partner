from typing import Optional

from mung_manager.reservations.models import Reservation
from mung_manager.reservations.selectors.abstracts import AbstractReservationSelector


class ReservationSelector(AbstractReservationSelector):
    """이 클래스는 예약을 DB에서 PULL하는 비즈니스 로직을 담당합니다."""

    def get_reservation_list(self, pet_kindergarden_id: int, reserved_at: str) -> dict[str, list[Reservation]]:
        """예약 리스트를 조회합니다.

        Args:
            pet_kindergarden_id (int): 반려동물 유치원 아이디
            reserved_at (str): 예약 날짜

        Returns:
            dict: 예약 리스트를 'time', 'all_day', 'hotel' 키로 구분하여 반환하며, 존재하지 않으면 빈 리스트 반환
        """
        reservations = Reservation.objects.filter(
            pet_kindergarden_id=pet_kindergarden_id,
            reserved_at=reserved_at,
        ).select_related(
            "customer",
            "customer_pet",
            "customer_ticket",
            "customer_ticket__ticket",
        )

        time_reservations = []
        all_day_reservations = []
        hotel_reservations = []

        for reservation in reservations:
            ticket_type = reservation.customer_ticket.ticket.ticket_type
            if ticket_type == "시간":
                time_reservations.append(reservation)
            elif ticket_type == "종일":
                all_day_reservations.append(reservation)
            elif ticket_type == "호텔":
                hotel_reservations.append(reservation)

        return {"time": time_reservations, "all_day": all_day_reservations, "hotel": hotel_reservations}

    def get_reservation_by_id(self, reservation_id: int) -> Optional[Reservation]:
        """예약 아이디로 예약을 조회합니다.

        Args:
            reservation_id (int): 예약 아이디

        Returns:
            Optional[Reservation]: 예약이 존재하면 예약 객체를 반환하고, 존재하지 않으면 None을 반환
        """
        try:
            return Reservation.objects.filter(id=reservation_id).get()

        except Reservation.DoesNotExist:
            return None
