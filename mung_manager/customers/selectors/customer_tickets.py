from django.db.models.query import QuerySet

from mung_manager.customers.models import CustomerTicket
from mung_manager.customers.selectors.abstracts import AbstractCustomerTicketSelector


class CustomerTicketSelector(AbstractCustomerTicketSelector):
    """이 클래스는 고객 티켓을 데이터베이스에서 PULL하는 비즈니스 로직을 담당합니다."""

    def get_customer_ticket_with_ticket_queryset_by_customer_id(self, customer_id: int) -> QuerySet[CustomerTicket]:
        """이 함수는 고객 아이디로 티켓을 포함한 고객 티켓을 최신순으로 조회합니다.

        Args:
            customer_id: 고객 아이디

        Returns:
            QuerySet[CustomerTicket]: 고객 티켓 쿼리셋이며 없을 경우 빈 쿼리셋을 반환
        """
        return CustomerTicket.objects.filter(customer_id=customer_id).select_related("ticket").order_by("-created_at")
