from enum import Enum


class ReservationStatus(Enum):
    """예약 상태"""

    PENDING = "대기"
    CANCELED = "취소"
    COMPLETED = "완료"
    EXPIRED = "만료"
