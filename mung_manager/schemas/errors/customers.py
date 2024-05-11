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

ErrorCustomerCsvFileEmptySchema = OpenApiExample(
    name="400(csv_file_empty)",
    summary="[Validation Failed]: CSV File Empty",
    description="""
    CSV 파일이 비어있을 때 반환되는 응답입니다.
    """,
    value={
        "success": False,
        "statusCode": 400,
        "code": "validation_failed",
        "message": "CSV file is empty.",
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
