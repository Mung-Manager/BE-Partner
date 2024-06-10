from drf_spectacular.utils import OpenApiExample

ErrorDayOffNotFoundSchema = OpenApiExample(
    name="404(day_off_not_found)",
    summary="[Not Found]: Day Off Not Found",
    description="""
    해당 휴무일을 찾을 수 없을 때 반환되는 응답입니다.
    """,
    value={
        "success": False,
        "statusCode": 404,
        "code": "not_found_day_off",
        "message": "Day Off does not exist.",
        "data": {},
    },
    status_codes=["404"],
    response_only=True,
)

ErrorDayOffAlreadyExistsSchema = OpenApiExample(
    name="400(day_off_already_exists)",
    summary="[Already Exists]: Day Off Already Exists",
    description="""
    해당 휴무일이 이미 존재할 때 반환되는 응답입니다.
    """,
    value={
        "success": False,
        "statusCode": 400,
        "code": "already_exists_day_off",
        "message": "Day Off already exists.",
        "data": {},
    },
    status_codes=["400"],
    response_only=True,
)

ErrorReservationNotFoundSchema = OpenApiExample(
    name="404(reservation_not_found)",
    summary="[Not Found]: Reservation Not Found",
    description="""
    해당 예약을 찾을 수 없을 때 반환되는 응답입니다.
    """,
    value={
        "success": False,
        "statusCode": 404,
        "code": "not_found_reservation",
        "message": "Reservation does not exist.",
        "data": {},
    },
    status_codes=["404"],
    response_only=True,
)

ErrorReservationAlreadyExistsCustomerPetSchema = OpenApiExample(
    name="400(reservation_already_exists_customer_pet)",
    summary="[Already Exists]: Reservation Already Exists Customer Pet",
    description="""
    해당 고객 반려동물에 대한 예약이 이미 존재할 때 반환되는 응답입니다.
    """,
    value={
        "success": False,
        "statusCode": 400,
        "code": "already_exists_reservation_customer_pet",
        "message": "Reservation already exists for customer pet.",
        "data": {},
    },
    status_codes=["400"],
    response_only=True,
)

ErrorReservationTimeTicketTypeAllDaySchema = OpenApiExample(
    name="400(reservation_time_ticket_type_all_day)",
    summary="[Validation Failed]: Reservation Time Ticket Type All Day",
    description="""
    해당 티켓 타입이 하루 종일 사용 가능한 경우, 예약 시간이 하루 종일인지 확인하는 응답입니다.
    """,
    value={
        "success": False,
        "statusCode": 400,
        "code": "validation_failed",
        "message": "The reservation time must be on the same day, with start at 00:00 and end at 23:59.",
        "data": {},
    },
    status_codes=["400"],
    response_only=True,
)

ErrorReservationTimeTicketTypeHotelSchema = OpenApiExample(
    name="400(reservation_time_ticket_type_hotel)",
    summary="[Validation Failed]: Reservation Time Ticket Type Hotel",
    description="""
    해당 티켓 타입이 호텔인 경우, 예약 시간이 1일 이내인지 확인하는 응답입니다.
    """,
    value={
        "success": False,
        "statusCode": 400,
        "code": "validation_failed",
        "message": "Reservations are not available within 1 day.",
        "data": {},
    },
    status_codes=["400"],
    response_only=True,
)

ErrorReservationTimeTicketTypeTimeSchema = OpenApiExample(
    name="400(reservation_time_ticket_type_time)",
    summary="[Validation Failed]: Reservation Time Ticket Type Time",
    description="""
    해당 티켓 타입이 시간제한이 있는 경우, 예약 시간이 티켓 사용 시간과 일치하는지 확인하는 응답입니다.
    """,
    value={
        "success": False,
        "statusCode": 400,
        "code": "validation_failed",
        "message": "The reservation time must match the ticket usage time.",
        "data": {},
    },
    status_codes=["400"],
    response_only=True,
)
