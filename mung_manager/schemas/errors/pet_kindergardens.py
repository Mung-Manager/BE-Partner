from drf_spectacular.utils import OpenApiExample

ErrorPetKindergardenNotFoundSchema = OpenApiExample(
    name="404(pet_kindergarden_not_found)",
    summary="[Not Found]: Pet Kindergarden Not Found",
    description="""
    해당 반려동물 유치원을 찾을 수 없을 때 반환되는 응답입니다.
    """,
    value={
        "success": False,
        "statusCode": 404,
        "code": "not_found_pet_kindergarden",
        "message": "Pet Kindergarden does not exist.",
        "data": {},
    },
    status_codes=["404"],
    response_only=True,
)

ErrorPetKindergardenAlreadyExistsSchema = OpenApiExample(
    name="409(pet_kindergarden_already_exists)",
    summary="[Conflict]: Pet Kindergarden Already Exists",
    description="""
    유저가 반려동물 유치원을 이미 가지고 있을 때 반환되는 응답입니다.
    """,
    value={
        "success": False,
        "statusCode": 409,
        "code": "already_exists_pet_kindergarden",
        "message": "User already has a pet kindergarden.",
        "data": {},
    },
    status_codes=["409"],
    response_only=True,
)

ErrorPetKindergardenClosedSchema = OpenApiExample(
    name="400(pet_kindergarden_closed)",
    summary="[Bad Request]: Pet Kindergarden Closed",
    description="""
    반려동물 유치원이 휴원일일 때 반환되는 응답입니다.
    """,
    value={
        "success": False,
        "statusCode": 400,
        "code": "pet_kindergarden_closed",
        "message": "The pet kindergarden is closed on this day.",
        "data": {},
    },
    status_codes=["400"],
    response_only=True,
)

ErrorPetKindergardenInvalidBusinessHourSchema = OpenApiExample(
    name="400(invalid_pet_kindergarden_business_hour)",
    summary="[Bad Request]: Invalid Pet Kindergarden Business Hour",
    description="""
    반려동물 유치원의 영업시간이 잘못되었을 때 반환되는 응답입니다.
    """,
    value={
        "success": False,
        "statusCode": 400,
        "code": "invalid_pet_kindergarden_business_hour",
        "message": "Invalid Pet Kindergarden Business Hour.",
        "data": {},
    },
    status_codes=["400"],
    response_only=True,
)
