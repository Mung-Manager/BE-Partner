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
