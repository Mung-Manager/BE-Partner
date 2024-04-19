import pytest
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.test import APIRequestFactory
from rest_framework.views import APIView

from mung_manager.common.pagination import LimitOffsetPagination, get_paginated_data
from mung_manager.users.models import User

factory = APIRequestFactory()
pytestmark = pytest.mark.django_db


class LimitOffsetExampleListApi(APIView):
    class Pagination(LimitOffsetPagination):
        default_limit = 1

    class OutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = User
            fields = ("id", "email")

    def get(self, request):
        queryset = User.objects.order_by("id")

        data = get_paginated_data(
            pagination_class=self.Pagination,
            serializer_class=self.OutputSerializer,
            queryset=queryset,
            request=request,
            view=self,
        )

        return Response(data=data, status=status.HTTP_200_OK)


class TestLimitOffsetPagination:
    def test_response_is_paginated_correctly(self, active_guest_user, active_partner_user):
        request = factory.get("/some/path")
        view = LimitOffsetExampleListApi.as_view()
        response = view(request)

        assert response.status_code == 200

        data = response.data

        assert data["limit"] == 1
        assert data["offset"] == 0
        assert data["count"] == 2
        assert data["next"] == "http://testserver/some/path?limit=1&offset=1"
        assert data["previous"] is None

        results = data["results"]

        assert len(results) == 1

        next_page_request = factory.get("/some/path?limit=1&offset=1")
        next_page_response = view(next_page_request)

        assert next_page_response.status_code == 200

        next_page_data = next_page_response.data

        assert next_page_data["limit"] == 1
        assert next_page_data["offset"] == 1
        assert next_page_data["count"] == 2
        assert next_page_data["next"] is None
        assert next_page_data["previous"] == "http://testserver/some/path?limit=1"

        next_page_results = next_page_data["results"]

        assert len(next_page_results) == 1
