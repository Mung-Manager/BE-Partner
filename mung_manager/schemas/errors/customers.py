from drf_spectacular.utils import OpenApiExample

ErrorCustomerNotFoundSchema = OpenApiExample(
    name="404(customer_not_found)",
    summary="[Not Found]: Customer Not Found",
    description="""
    해당 고객을 찾을 수 없을 때 반환되는 응답입니다.
    """,
    value={
        "success": False,
        "statusCode": 404,
        "code": "not_found_customer",
        "message": "Customer does not exist.",
        "data": {},
    },
    status_codes=["404"],
    response_only=True,
)

ErrorCustomerAlreadyExistsSchema = OpenApiExample(
    name="400(customer_already_exists)",
    summary="[Already Exists]: Customer Already Exists",
    description="""
    유저가 이미 고객을 가지고 있을 때 반환되는 응답입니다.
    """,
    value={
        "success": False,
        "statusCode": 400,
        "code": "already_exists_customer",
        "message": "User already has a customer.",
        "data": {},
    },
    status_codes=["400"],
    response_only=True,
)

ErrorCustomerCsvPhoneNumberDuplicatedSchema = OpenApiExample(
    name="400(csv_phone_number_duplicated)",
    summary="[Validation Failed]: CSV Phone Number Duplicated",
    description="""
    CSV 파일에 중복된 전화번호가 있을 때 반환되는 응답입니다.
    """,
    value={
        "success": False,
        "statusCode": 400,
        "code": "validation_failed",
        "message": "Csv file phone number is duplicated.",
        "data": {},
    },
    status_codes=["400"],
    response_only=True,
)

ErrorCustomerPetNameDuplicatedSchema = OpenApiExample(
    name="400(pet_name_duplicated)",
    summary="[Validation Failed]: Pet Name Duplicated",
    description="""
    반려동물 이름이 중복될 때 반환되는 응답입니다.
    """,
    value={
        "success": False,
        "statusCode": 400,
        "code": "unique_pet_name",
        "message": "Customer pet names must be unique.",
        "data": {},
    },
    status_codes=["400"],
    response_only=True,
)


ErrorCustomerPetAlreadyExistsSchema = OpenApiExample(
    name="400(pet_already_exists)",
    summary="[Already Exists]: Pet Already Exists",
    description="""
    유저가 이미 반려동물을 가지고 있을 때 반환되는 응답입니다.
    """,
    value={
        "success": False,
        "statusCode": 400,
        "code": "already_exists_customer_pet",
        "message": "Customer pet already exists.",
        "data": {},
    },
    status_codes=["400"],
    response_only=True,
)

ErrorCustomerPetOverDailyLimitSchema = OpenApiExample(
    name="400(pet_over_daily_limit)",
    summary="[Validation Failed]: Pet Over Daily Limit",
    description="""
    반려동물 등록 제한을 초과할 때 반환되는 응답입니다.
    """,
    value={
        "success": False,
        "statusCode": 400,
        "code": "over_daily_limit",
        "message": "The daily pet limit has been exceeded",
        "data": {},
    },
    status_codes=["400"],
    response_only=True,
)

ErrorCustomerTicketNotFoundSchema = OpenApiExample(
    name="404(ticket_not_found)",
    summary="[Not Found]: Ticket Not Found",
    description="""
    해당 티켓을 찾을 수 없을 때 반환되는 응답입니다.
    """,
    value={
        "success": False,
        "statusCode": 404,
        "code": "not_found_customer_ticket",
        "message": "Customer ticket does not exist.",
        "data": {},
    },
    status_codes=["404"],
    response_only=True,
)

ErrorCustomerTicketExpiredSchema = OpenApiExample(
    name="400(ticket_expired)",
    summary="[Bad Request]: Ticket Expired",
    description="""
    티켓이 만료되었을 때 반환되는 응답입니다.
    """,
    value={
        "success": False,
        "statusCode": 400,
        "code": "expired_customer_ticket",
        "message": "Customer ticket has expired.",
        "data": {},
    },
    status_codes=["400"],
    response_only=True,
)

ErrorCustomerTicketInvalidExpiredAtSchema = OpenApiExample(
    name="400(invalid_ticket_expired_at)",
    summary="[Validation Failed]: Invalid Ticket Expired At",
    description="""
    티켓 만료일 내에 예약일이 있어야 할 때 반환되는 응답입니다.
    """,
    value={
        "success": False,
        "statusCode": 400,
        "code": "invalid_customer_ticket_expired_at",
        "message": "The reservation date must be within the expiration date of the ticket.",
        "data": {},
    },
    status_codes=["400"],
    response_only=True,
)

ErrorCustomerTicketNoCountSchema = OpenApiExample(
    name="400(no_ticket_count)",
    summary="[Validation Failed]: No Ticket Count",
    description="""
    남은 티켓 카운트가 없을 때 반환되는 응답입니다.
    """,
    value={
        "success": False,
        "statusCode": 400,
        "code": "no_customer_ticket_count",
        "message": "There are no remaining ticket counts.",
        "data": {},
    },
    status_codes=["400"],
    response_only=True,
)

ErrorCustomerTicketConflictSchema = OpenApiExample(
    name="409(conflict_ticket)",
    summary="[Conflict]: Conflict Ticket",
    description="""
    예약 등록에 실패했을 때 반환되는 응답입니다.
    """,
    value={
        "success": False,
        "statusCode": 409,
        "code": "conflict_customer_ticket",
        "message": "Reservation failed to register, please try again.",
        "data": {},
    },
    status_codes=["409"],
    response_only=True,
)
