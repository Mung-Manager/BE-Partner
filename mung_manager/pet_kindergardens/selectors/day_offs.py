from django.db.models.query import QuerySet

from mung_manager.pet_kindergardens.models import DayOff
from mung_manager.pet_kindergardens.selectors.abstracts import AbstractDayOffSelector


class DayOffSelector(AbstractDayOffSelector):
    def get_day_off_queryset_by_pet_kindergarden_id_and_day_off_at(
        self, pet_kindergarden_id: int, year: int, month: int
    ) -> QuerySet[DayOff]:
        """반려동물 유치원 아이디와 년도와 월로 휴무일 리스트를 조회합니다.

        Args:
            pet_kindergarden_id (int): 반려동물 유치원 아이디
            year (int): 년도
            month (int): 월

        Returns:
            QuerySet[DayOff]: 휴무일 리스트 쿼리셋이며 존재하지 않으면 빈 쿼리셋을 반환
        """
        return DayOff.objects.filter(
            pet_kindergarden_id=pet_kindergarden_id, day_off_at__year=year, day_off_at__month=month
        )
