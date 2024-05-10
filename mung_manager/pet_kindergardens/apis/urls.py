from django.urls import path

from mung_manager.pet_kindergardens.apis.customers.api_managers import (
    CustomerBatchRegisterAPIManager,
    CustomerDetailAPIManager,
    CustomerListAPIManager,
    CustomerPetDetailAPIManager,
    CustomerTicketActiveListAPIManager,
    CustomerTicketDetailAPIManager,
    CustomerTicketListAPIManager,
    CustomerTicketLogListAPIManger,
    CustomerToggleActiveAPIManager,
)
from mung_manager.pet_kindergardens.apis.pet_kindergardens.api_managers import (
    PetkindergardenListAPIManager,
    PetkindergardenProfileAPIManager,
    PetkindergardenSearchAPIManager,
)
from mung_manager.pet_kindergardens.apis.reservations.api_managers import (
    ReservationCalendarListAPIManager,
)
from mung_manager.pet_kindergardens.apis.tickets.api_managers import (
    TicketDetailManagerAPI,
    TicketListAPIManager,
)

pet_kindergarden_urls = [
    path(
        "",
        PetkindergardenListAPIManager.as_view(),
        name="pet-kindergarden-list",
    ),
    path(
        "/search",
        PetkindergardenSearchAPIManager.as_view(),
        name="pet-kindergarden-search",
    ),
    path(
        "/profile",
        PetkindergardenProfileAPIManager.as_view(),
        name="pet-kindergarden-profile",
    ),
]

pet_kindergarden_ticket_urls = [
    path(
        "/<int:pet_kindergarden_id>/tickets",
        TicketListAPIManager.as_view(),
        name="pet-kindergarden-tickets-list",
    ),
    path(
        "/<int:pet_kindergarden_id>/tickets/<int:ticket_id>",
        TicketDetailManagerAPI.as_view(),
        name="pet-kindergarden-tickets-detail",
    ),
]
pet_kindergarden_customer_urls = [
    path(
        "/<int:pet_kindergarden_id>/customers",
        CustomerListAPIManager.as_view(),
        name="pet-kindergarden-customers-list",
    ),
    path(
        "/<int:pet_kindergarden_id>/customers/batch-register",
        CustomerBatchRegisterAPIManager.as_view(),
        name="pet-kindergarden-customers-batch-register",
    ),
    path(
        "/<int:pet_kindergarden_id>/customers/tickets",
        CustomerTicketActiveListAPIManager.as_view(),
        name="pet-kindergarden-customers-tickets-list",
    ),
    path(
        "/<int:pet_kindergarden_id>/customers/<int:customer_id>",
        CustomerDetailAPIManager.as_view(),
        name="pet-kindergarden-customers-detail",
    ),
    path(
        "/<int:pet_kindergarden_id>/customers/<int:customer_id>/toggle-is-active",
        CustomerToggleActiveAPIManager.as_view(),
        name="pet-kindergarden-customers-detail-toggle-is-active",
    ),
    path(
        "/<int:pet_kindergarden_id>/customers/<int:customer_id>/pets/<int:pet_id>",
        CustomerPetDetailAPIManager.as_view(),
        name="pet-kindergarden-customers-pets-detail",
    ),
    path(
        "/<int:pet_kindergarden_id>/customers/<int:customer_id>/tickets",
        CustomerTicketListAPIManager.as_view(),
        name="pet-kindergarden-customers-tickets-list",
    ),
    path(
        "/<int:pet_kindergarden_id>/customers/<int:customer_id>/tickets/<int:ticket_id>",
        CustomerTicketDetailAPIManager.as_view(),
        name="pet-kindergarden-customers-tickets-detail",
    ),
    path(
        "/<int:pet_kindergarden_id>/customers/<int:customer_id>/tickets/logs",
        CustomerTicketLogListAPIManger.as_view(),
        name="pet-kindergarden-customers-tickets-logs-list",
    ),
]

pet_kindergarden_reservation_urls = [
    path(
        "/<int:pet_kindergarden_id>/reservations/calendar",
        ReservationCalendarListAPIManager.as_view(),
        name="pet-kindergarden-reservations-calendar",
    ),
]

urlpatterns = (
    pet_kindergarden_urls
    + pet_kindergarden_ticket_urls
    + pet_kindergarden_customer_urls
    + pet_kindergarden_reservation_urls
)
