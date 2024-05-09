from django.db.models.query import QuerySet

from mung_manager.customers.models import CustomerTicketReservation
from mung_manager.customers.selectors.abstracts import (
    AbstractCustomerTicketReservationSelector,
)


class CustomerTicketReservationSelector(AbstractCustomerTicketReservationSelector):
    """이 클래스는 고객 티켓 예약을 데이터베이스에서 PULL하는 비즈니스 로직을 담당합니다."""

    def get_customer_ticket_reservation_list_by_customer_id(
        self, customer_id: int
    ) -> QuerySet[CustomerTicketReservation]:
        """이 함수는 고객 아이디로 고객 티켓, 티켓, 예약을 포함한 고객 티켓 예약을 최신순으로 조회합니다.

        Args:
            customer_id (int): 고객 아이디

        Returns:
            QuerySet[CustomerTicketReservation]: 고객 티켓 예약 쿼리셋이며 존재하지 않으면 빈 쿼리셋을 반환
        """
        return (
            CustomerTicketReservation.objects.filter(customer_ticket__customer_id=customer_id)
            .select_related("customer_ticket", "customer_ticket__ticket", "reservation")
            .order_by("-created_at")
        )
