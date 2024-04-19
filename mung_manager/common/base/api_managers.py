from rest_framework import status
from rest_framework.views import APIView

from mung_manager.common.exception.exceptions import NotImplementedException
from mung_manager.common.response import create_response


class BaseAPIManager(APIView):
    VIEWS_BY_METHOD: dict = dict()
    """이 클래스는 APIView 클래스를 단일 URL(GET, PUT)로 관리하기 위한 클래스입니다.

    Attributes:
        VIEWS_BY_METHOD (dict): HTTP 메소드 별로 호출할 APIView 클래스를 정의

    Examples:
        VIEWS_BY_METHOD = {
            'GET': ListAPI.as_view,
            'POST': CreateAPI.as_view,
        }
    """

    def dispatch(self, request, *args, **kwargs):
        if not hasattr(self, "VIEWS_BY_METHOD"):
            raise NotImplementedException("VIEWS_BY_METHOD should be defined in the subclass")

        if request.method in self.VIEWS_BY_METHOD:
            return self.VIEWS_BY_METHOD[request.method]()(request, *args, **kwargs)
        return create_response(
            message="Method not allowed",
            status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
        )
