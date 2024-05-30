from typing import TypedDict

from django.db.models import F
from django.db.models.query import QuerySet
from django.utils import timezone
from django_stubs_ext import WithAnnotations

from mung_manager.customers.models import CustomerTicket
from mung_manager.customers.selectors.abstracts import AbstractCustomerTicketSelector


class CustomerTicketAnnotation(TypedDict):
    unused_count: int


class CustomerTicketSelector(AbstractCustomerTicketSelector):
    """이 클래스는 고객 티켓을 DB에서 PULL하는 비즈니스 로직을 담당합니다."""

    def get_customer_ticket_with_ticket_queryset_by_customer_id(self, customer_id: int) -> QuerySet[CustomerTicket]:
        """이 함수는 고객 아이디로 티켓을 포함한 고객 티켓을 최신순으로 조회합니다.

        Args:
            customer_id: 고객 아이디

        Returns:
            QuerySet[CustomerTicket]: 고객 티켓 쿼리셋이며 없을 경우 빈 쿼리셋을 반환
        """
        return CustomerTicket.objects.filter(customer_id=customer_id).select_related("ticket").order_by("-created_at")

    def get_customer_ticket_list_by_customer_id_for_reservation(
        self, customer_id: int
    ) -> dict[str, list[WithAnnotations[CustomerTicket, CustomerTicketAnnotation]]]:
        """이 함수는 고객 아이디로 예약을 위한 티켓을 포함한 만료기간 및 사용횟수가 남은 고객 티켓을 조회합니다.
        사용하지 않은 횟수를 계산하여 반환합니다.

        Args:
            customer_id: 고객 아이디

        Returns:
            QuerySet[CustomerTicket]: 고객 티켓 쿼리셋이며 없을 경우 빈 쿼리셋을 반환
        """
        customer_tickets = (
            CustomerTicket.objects.filter(
                customer_id=customer_id,
                expired_at__gte=timezone.now(),
                total_count__gt=F("used_count"),
            )
            .select_related("ticket")
            .annotate(unused_count=F("total_count") - F("used_count"))
        )
        time_customer_tickets = []
        all_day_customer_tickets = []
        hotel_customer_tickets = []

        for customer_ticket in customer_tickets:
            ticket_type = customer_ticket.ticket.ticket_type
            if ticket_type == "시간":
                time_customer_tickets.append(customer_ticket)
            elif ticket_type == "종일":
                all_day_customer_tickets.append(customer_ticket)
            elif ticket_type == "호텔":
                hotel_customer_tickets.append(customer_ticket)

        return {
            "time": time_customer_tickets,
            "all_day": all_day_customer_tickets,
            "hotel": hotel_customer_tickets,
        }
