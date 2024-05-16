from django.db.models.query import QuerySet

from mung_manager.reservations.models import Reservation
from mung_manager.reservations.selectors.abstracts import AbstractReservationSelector


class ReservationSelector(AbstractReservationSelector):
    def get_reservation_list(self, pet_kindergarden_id: int, reserved_at: str) -> QuerySet[Reservation]:
        return Reservation.objects.filter(
            pet_kindergarden_id=pet_kindergarden_id,
            reserved_at=reserved_at,
        ).select_related(
            "customer",
            "customer_pet",
            "customer_ticket",
        )
