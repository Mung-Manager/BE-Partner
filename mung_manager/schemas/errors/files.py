from drf_spectacular.utils import OpenApiExample

ErrorFileMaxSizeExceededSchema = OpenApiExample(
    name="400(file_max_size_exceeded)",
    summary="[Validation Failed]: File Max Size Exceeded",
    description="""
    파일의 크기가 설정된 최대 크기를 넘었을 때 반환되는 응답입니다.
    """,
    value={
        "success": False,
        "statusCode": 400,
        "code": "validation_failed",
        "message": "File is too large. It should not exceed {max_size} MiB",
        "data": {},
    },
    status_codes=["400"],
    response_only=True,
)

ErrorImageInvalidSchema = OpenApiExample(
    name="400(image_invalid)",
    summary="[Validation Failed]: Image Invalid",
    description="""
    이미지 파일이 아닌 경우 반환되는 응답입니다.
    """,
    value={
        "success": False,
        "statusCode": 400,
        "code": "validation_failed",
        "message": "Invalid file type: {error}",
        "data": {},
    },
    status_codes=["400"],
    response_only=True,
)

ErrorFildUploadFailedSchema = OpenApiExample(
    name="500(file_upload_failed)",
    summary="[Validation Failed]: File Upload Failed",
    description="""
    파일 업로드에 실패했을 때 반환되는 응답입니다.
    """,
    value={
        "success": False,
        "statusCode": 400,
        "code": "validation_failed",
        "message": "{error}",
        "data": {},
    },
    status_codes=["400"],
    response_only=True,
)
