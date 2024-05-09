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
        "message": "Pet Kindergarden not found",
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
