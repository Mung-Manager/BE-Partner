from django.db.models.query import QuerySet

from mung_manager.reservations.models import DailyReservation
from mung_manager.reservations.selectors.abstracts import (
    AbstractDailyReservationSelector,
)


class DailyReservationSelector(AbstractDailyReservationSelector):
    """이 클래스는 일별 예약을 DB에서 PULL하는 비즈니스 로직을 담당합니다."""

    def get_daily_reservations_queryset_by_year_and_month_and_pet_kindergarden_id(
        self, year: int, month: int, pet_kindergarden_id: int
    ) -> QuerySet[DailyReservation]:
        """년도와 월과 반려동물 유치원 아이디로 일별 예약 리스트를 조회합니다.

        Args:
            year (int): 년도
            month (int): 월
            pet_kindergarden_id (int): 반려동물 유치원 아이디

        Returns:
            QuerySet[DailyReservation]: 일별 예약 리스트 쿼리셋이며 존재하지 않으면 빈 쿼리셋을 반환
        """
        return DailyReservation.objects.filter(
            reserved_at__year=year, reserved_at__month=month, pet_kindergarden_id=pet_kindergarden_id
        )
