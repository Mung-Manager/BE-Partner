from django.db.models.query import QuerySet

from mung_manager.customers.models import CustomerTicketLog
from mung_manager.customers.selectors.abstracts import AbstractCustomerTicketLogSelector


class CustomerTicketLogSelector(AbstractCustomerTicketLogSelector):
    """이 클래스는 고객 티켓 로그를 데이터베이스에서 PULL하는 비즈니스 로직을 담당합니다."""

    def get_customer_ticket_log_with_customer_ticket_and_ticket_queryset_by_customer_id_order_by_created_at_desc(
        self, customer_id: int
    ) -> QuerySet[CustomerTicketLog]:
        """이 함수는 고객 아이디로 고객 티켓, 티켓을 포함한 고객 티켓 로그를 최신순으로 조회합니다.

        Args:
            customer_id (int): 고객 아이디

        Returns:
            QuerySet[CustomerTicketLog]: 고객 티켓 로그 쿼리셋이며 존재하지 않으면 빈 쿼리셋을 반환
        """
        return (
            CustomerTicketLog.objects.filter(customer_ticket__customer_id=customer_id)
            .select_related("customer_ticket", "customer_ticket__ticket")
            .order_by("-created_at")
        )
