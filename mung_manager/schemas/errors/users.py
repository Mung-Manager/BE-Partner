from drf_spectacular.utils import OpenApiExample

ErrorEmailAlreadyExistSchema = OpenApiExample(
    name="400(email_already_exist)",
    summary="[Already Exist]: Email already exist",
    description="""
    이메일이 이미 존재할 때 반환되는 응답입니다.
    """,
    value={
        "success": False,
        "statusCode": 400,
        "code": "already_exist",
        "message": "Email already exist.",
        "data": {},
    },
    status_codes=["400"],
    response_only=True,
)
