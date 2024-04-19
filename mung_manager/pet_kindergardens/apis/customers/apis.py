from django.utils import timezone
from rest_framework import serializers, status
from rest_framework.parsers import MultiPartParser
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from mung_manager.common.base.serializers import BaseSerializer
from mung_manager.common.exception.exceptions import NotFoundException
from mung_manager.common.mixins import APIAuthMixin
from mung_manager.common.pagination import LimitOffsetPagination, get_paginated_data
from mung_manager.common.response import create_response
from mung_manager.common.utils import inline_serializer
from mung_manager.common.validators import PhoneNumberValidator
from mung_manager.customers.containers import CustomerContainer
from mung_manager.pet_kindergardens.containers import PetKindergardenContainer
from mung_manager.tickets.containers import TicketContainer


class CustomerListAPI(APIAuthMixin, APIView):
    class Pagination(LimitOffsetPagination):
        default_limit = 10

    class FilterSerializer(BaseSerializer):
        customer_name = serializers.CharField(required=False)
        customer_phone_number = serializers.CharField(required=False)
        customer_pet_name = serializers.CharField(required=False)
        ticket_id = serializers.IntegerField(required=False)
        is_active = serializers.BooleanField(required=True)
        limit = serializers.IntegerField(default=10, min_value=1, max_value=50)
        offset = serializers.IntegerField(default=0, min_value=0)

    class OutputSerializer(BaseSerializer):
        id = serializers.IntegerField()
        name = serializers.CharField()
        phone_number = serializers.CharField()
        customer_pets = inline_serializer(
            many=True,
            fields={
                "id": serializers.IntegerField(),
                "name": serializers.CharField(),
            },
            source="undeleted_customer_pets",
        )
        customer_tickets = inline_serializer(
            many=True,
            fields={
                "id": serializers.IntegerField(),
                "total_count": serializers.IntegerField(),
                "used_count": serializers.IntegerField(),
                "ticket": inline_serializer(
                    fields={
                        "id": serializers.IntegerField(),
                        "ticket_type": serializers.CharField(),
                        "usage_count": serializers.IntegerField(),
                        "usage_time_count": serializers.IntegerField(),
                        "usage_period_in_days_count": serializers.IntegerField(),
                    }
                ),
            },
        )
        memo = serializers.CharField()
        # recent_reserved_at = serializers.SerializerMethodField() #@TODO: 컬럼 추가
        created_at = serializers.DateTimeField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._pet_kindergarden_selector = PetKindergardenContainer.pet_kindergarden_selector()
        self._customer_selector = CustomerContainer.customer_selector()

    def get(self, request: Request, pet_kindergarden_id: int) -> Response:
        """
        유저가 반려동물 유치원 고객 목록을 조회합니다.
        url: /partners/pet-kindergardens/{pet_kindergarden_id}/customers

        Args:
            FilterSerializer: 반려동물 유치원 고객 목록 조회
                customer_name (str): 고객 이름
                customer_phone_number (str): 고객 전화번호
                customer_pet_name (str): 반려동물 이름
                ticket_id (int): 티켓 아이디
                is_active (bool): 활성화 여부
                limit (int): 페이지당 조회 개수
                offset (int): 페이지 오프셋
            pet_kindergarden_id (int): 반려동물 유치원 아이디

        Returns:
            OutputSerializer: 반려동물 유치원 고객 목록 조회 결과
                id (int): 고객 아이디
                name (str): 고객 이름
                phone_number (str): 고객 전화번호
                customer_pets (List[Dict]): 고객 반려동물 목록
                    id (int): 반려동물 아이디
                    name (str): 반려동물 이름
                customer_tickets (List[Dict]): 고객 티켓 목록
                    id (int): 티켓 아이디
                    total_count (int): 총 사용 가능 횟수
                    used_count (int): 사용 횟수
                    ticket (Dict): 티켓 정보
                        id (int): 티켓 아이디
                        ticket_type (str): 티켓 타입
                        usage_count (int): 사용 가능 횟수
                        usage_time_count (int): 사용 가능 시간
                        usage_period_in_days_count (int): 사용 가능 일수
                memo (str): 메모
                recent_reserved_at (datetime): 최근 예약 일시
                created_at (datetime): 생성 일시
        """
        filter_serializer = self.FilterSerializer(data=request.query_params)
        filter_serializer.is_valid(raise_exception=True)

        self._pet_kindergarden_selector.check_is_exists_pet_kindergarden_by_id_and_user(
            pet_kindergarten_id=pet_kindergarden_id,
            user=request.user,
        )
        customers = self._customer_selector.get_customer_list(filters=filter_serializer.validated_data)

        pagination_customers_data = get_paginated_data(
            pagination_class=self.Pagination,
            serializer_class=self.OutputSerializer,
            queryset=customers,
            request=request,
            view=self,
        )
        return create_response(data=pagination_customers_data, status_code=status.HTTP_200_OK)


class CustomerCreateAPI(APIAuthMixin, APIView):
    class InputSerializer(BaseSerializer):
        name = serializers.CharField(required=True, max_length=32)
        phone_number = serializers.CharField(required=True, min_length=11, max_length=16, validators=[PhoneNumberValidator()])
        pets = serializers.ListField(child=serializers.CharField(), required=True)

    class OutputSerializer(BaseSerializer):
        id = serializers.IntegerField()
        name = serializers.CharField()
        phone_number = serializers.CharField()
        customer_pets = inline_serializer(
            many=True,
            fields={
                "id": serializers.IntegerField(),
                "name": serializers.CharField(),
            },
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._customer_service = CustomerContainer.customer_service()

    def post(self, request: Request, pet_kindergarden_id: int) -> Response:
        """
        유저가 반려동물 유치원 고객을 생성합니다.
        url: /partners/pet-kindergardens/{pet_kindergarden_id}/customers

        Args:
            InputSerializer: 반려동물 유치원 고객 생성
                name (str): 고객 이름
                phone_number (str): 고객 전화번호
                pets (List[str]): 반려동물 이름 목록
            pet_kindergarden_id (int): 반려동물 유치원 아이디

        Returns:
            OutputSerializer: 반려동물 유치원 고객 생성 결과
                id (int): 고객 아이디
                name (str): 고객 이름
                phone_number (str): 고객 전화번호
                customer_pets (List[Dict]): 고객 반려동물 목록
                    id (int): 반려동물 아이디
                    name (str): 반려동물 이름
        """
        input_serializer = self.InputSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)

        customer = self._customer_service.create_customer(
            pet_kindergarden_id=pet_kindergarden_id,
            user=request.user,
            **input_serializer.validated_data,
        )

        customer_data = self.OutputSerializer(customer).data
        return create_response(data=customer_data, status_code=status.HTTP_201_CREATED)


class CustomerBatchRegisterAPI(APIAuthMixin, APIView):
    parser_classes = (MultiPartParser,)

    class InputSerializer(BaseSerializer):
        csv_file = serializers.FileField(required=True)

    class OutputSerializer(BaseSerializer):
        id = serializers.IntegerField()
        name = serializers.CharField()
        phone_number = serializers.CharField()
        customer_pets = inline_serializer(
            many=True,
            fields={
                "id": serializers.IntegerField(),
                "name": serializers.CharField(),
            },
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._customer_service = CustomerContainer.customer_service()

    def post(self, request: Request, pet_kindergarden_id: int) -> Response:
        """
        유저가 반려동물 유치원 고객을 CSV 파일로 일괄 생성합니다.
        url: /partners/pet-kindergardens/{pet_kindergarden_id}/customers/batch-register

        Args:
            InputSerializer: 반려동물 유치원 고객 일괄 생성
                csv_file (File): CSV 파일
            pet_kindergarden_id (int): 반려동물 유치원 아이디

        Returns:
            OutputSerializer: 반려동물 유치원 고객 일괄 생성 결과
                id (int): 고객 아이디
                name (str): 고객 이름
                phone_number (str): 고객 전화번호
                customer_pets (List[Dict]): 고객 반려동물 목록
                    id (int): 반려동물 아이디
                    name (str): 반려동물 이름
        """
        customers = self._customer_service.create_customers_by_csv(
            pet_kindergarden_id=pet_kindergarden_id,
            user=request.user,
            csv_file=request.FILES.get("csv_file"),
        )

        customers_data = self.OutputSerializer(customers, many=True).data
        return create_response(data=customers_data, status_code=status.HTTP_201_CREATED)


class CustomerDetailAPI(APIAuthMixin, APIView):
    class OutputSerializer(BaseSerializer):
        id = serializers.IntegerField()
        name = serializers.CharField()
        phone_number = serializers.CharField()
        customer_pets = inline_serializer(
            many=True,
            fields={
                "id": serializers.IntegerField(),
                "name": serializers.CharField(),
            },
            source="undeleted_customer_pets",
        )
        memo = serializers.CharField()
        created_at = serializers.DateTimeField()
        is_active = serializers.BooleanField()
        is_kakao_user = serializers.SerializerMethodField()

        def get_is_kakao_user(self, obj) -> bool:
            return obj.user is None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._pet_kindergarden_selector = PetKindergardenContainer.pet_kindergarden_selector()
        self._customer_selector = CustomerContainer.customer_selector()

    def get(self, request: Request, pet_kindergarden_id: int, customer_id: int) -> Response:
        """
        유저가 반려동물 유치원 고객 상세 정보를 조회합니다.
        url: /partners/pet-kindergardens/{pet_kindergarden_id}/customers/{customer_id}

        Args:
            pet_kindergarden_id (int): 반려동물 유치원 아이디
            customer_id (int): 고객 아이디

        Returns:
            OutputSerializer: 반려동물 유치원 고객 상세 정보 조회 결과
                id (int): 고객 아이디
                name (str): 고객 이름
                phone_number (str): 고객 전화번호
                customer_pets (List[Dict]): 고객 반려동물 목록
                    id (int): 반려동물 아이디
                    name (str): 반려동물 이름
                memo (str): 메모
                created_at (datetime): 생성 일시
                is_active (bool): 활성화 여부
                is_kakao_user (bool): 카카오 유저 여부
        """
        self._pet_kindergarden_selector.check_is_exists_pet_kindergarden_by_id_and_user(
            pet_kindergarten_id=pet_kindergarden_id,
            user=request.user,
        )
        customer = self._customer_selector.get_customer_with_undeleted_customer_pet_by_id(
            customer_id=customer_id,
        )
        if customer is None:
            raise NotFoundException(detail="Customer does not exist.", code="not_found_customer")

        customer_data = self.OutputSerializer(customer).data
        return create_response(data=customer_data, status_code=status.HTTP_200_OK)


class CustomerToggleActiveAPI(APIAuthMixin, APIView):
    class OutputSerializer(BaseSerializer):
        id = serializers.IntegerField()
        is_active = serializers.BooleanField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._customer_service = CustomerContainer.customer_service()

    def patch(self, request: Request, pet_kindergarden_id: int, customer_id: int) -> Response:
        """
        유저가 반려동물 유치원 고객 활성화 여부를 토글합니다.
        url: /partners/pet-kindergardens/{pet_kindergarden_id}/customers/{customer_id}

        Args:
            pet_kindergarden_id (int): 반려동물 유치원 아이디
            customer_id (int): 고객 아이디

        Returns:
            OutputSerializer: 반려동물 유치원 고객 활성화 여부 토글 결과
                id (int): 고객 아이디
                is_active (bool): 활성화 여부
        """
        customer = self._customer_service.toggle_customer_is_active(
            pet_kindergarden_id=pet_kindergarden_id,
            user=request.user,
            customer_id=customer_id,
        )

        customer_data = self.OutputSerializer(customer).data
        return create_response(data=customer_data, status_code=status.HTTP_200_OK)


class CustomerUpdateAPI(APIAuthMixin, APIView):
    class InputSerializer(BaseSerializer):
        name = serializers.CharField(required=True)
        phone_number = serializers.CharField(required=True)
        pets = serializers.ListField(child=serializers.CharField(), required=True)
        memo = serializers.CharField(required=False, allow_blank=True)

    class OutputSerializer(BaseSerializer):
        id = serializers.IntegerField()
        name = serializers.CharField()
        phone_number = serializers.CharField()
        customer_pets = inline_serializer(
            many=True,
            fields={
                "id": serializers.IntegerField(),
                "name": serializers.CharField(),
            },
            source="undeleted_customer_pets",
        )
        memo = serializers.CharField()
        created_at = serializers.DateTimeField()
        is_active = serializers.BooleanField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._customer_service = CustomerContainer.customer_service()

    def put(self, request: Request, pet_kindergarden_id: int, customer_id: int) -> Response:
        """
        유저가 반려동물 유치원 고객 정보를 수정합니다.
        url: /partners/pet-kindergardens/{pet_kindergarden_id}/customers/{customer_id}

        Args:
            InputSerializer: 반려동물 유치원 고객 정보 수정
                name (str): 고객 이름
                phone_number (str): 고객 전화번호
                pets (List[str]): 반려동물 이름 목록
                memo (str): 메모
            pet_kindergarden_id (int): 반려동물 유치원 아이디
            customer_id (int): 고객 아이디

        Returns:
            OutputSerializer: 반려동물 유치원 고객 정보 수정 결과
                id (int): 고객 아이디
                name (str): 고객 이름
                phone_number (str): 고객 전화번호
                customer_pets (List[Dict]): 고객 반려동물 목록
                    id (int): 반려동물 아이디
                    name (str): 반려동물 이름
                memo (str): 메모
                created_at (datetime): 생성 일시
                is_active (bool): 활성화 여부
        """
        input_serializer = self.InputSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)

        customer = self._customer_service.update_customer(
            pet_kindergarden_id=pet_kindergarden_id,
            user=request.user,
            customer_id=customer_id,
            **input_serializer.validated_data,
        )

        customer_data = self.OutputSerializer(customer).data
        return create_response(data=customer_data, status_code=status.HTTP_200_OK)


class CustomerTicketActiveListAPI(APIAuthMixin, APIView):
    class OutputSerializer(BaseSerializer):
        id = serializers.IntegerField()
        usage_time_count = serializers.IntegerField()
        usage_count = serializers.IntegerField()
        usage_period_in_days_count = serializers.IntegerField()
        price = serializers.IntegerField()
        ticket_type = serializers.CharField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._pet_kindergarden_selector = PetKindergardenContainer.pet_kindergarden_selector()
        self._ticket_selector = TicketContainer.ticket_selector()

    def get(self, request: Request, pet_kindergarden_id: int) -> Response:
        """
        유저가 반려동물 유치원 티켓 목록을 조회합니다.
        url: /partners/pet-kindergardens/{pet_kindergarden_id}/tickets

        Args:
            pet_kindergarden_id (int): 반려동물 유치원 아이디

        Returns:
            OutputSerializer: 반려동물 유치원 티켓 목록 조회 결과
                id (int): 티켓 아이디
                usage_time_count (int): 사용 가능 시간
                usage_count (int): 사용 가능 횟수
                usage_period_in_days_count (int): 사용 가능 일수
                price (int): 가격
                ticket_type (str): 티켓 타입
        """
        self._pet_kindergarden_selector.check_is_exists_pet_kindergarden_by_id_and_user(
            pet_kindergarten_id=pet_kindergarden_id,
            user=request.user,
        )
        tickets = self._ticket_selector.get_undeleted_ticket_by_pet_kindergarden_id(
            pet_kindergarden_id=pet_kindergarden_id,
        )

        tickets_data = self.OutputSerializer(tickets, many=True).data
        return create_response(data=tickets_data, status_code=status.HTTP_200_OK)


class CustomerTicketListAPI(APIAuthMixin, APIView):
    class Pagination(LimitOffsetPagination):
        default_limit = 10

    class FilterSerializer(BaseSerializer):
        limit = serializers.IntegerField(default=10, min_value=1, max_value=50)
        offset = serializers.IntegerField(default=0, min_value=0)

    class OutputSerializer(BaseSerializer):
        id = serializers.IntegerField()
        usage_time_count = serializers.IntegerField(source="ticket.usage_time_count")
        usage_count = serializers.IntegerField(source="ticket.usage_count")
        usage_period_in_days_count = serializers.IntegerField(source="ticket.usage_period_in_days_count")
        price = serializers.IntegerField(source="ticket.price")
        ticket_type = serializers.CharField(source="ticket.ticket_type")
        created_at = serializers.DateTimeField()
        expired_at = serializers.DateTimeField()
        status = serializers.SerializerMethodField()

        def get_status(self, obj) -> str:
            if obj.expired_at < timezone.now():
                return "만료"
            return "이용중"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._pet_kindergarden_selector = PetKindergardenContainer.pet_kindergarden_selector()
        self._customer_selector = CustomerContainer.customer_selector()
        self._customer_ticket_selector = CustomerContainer.customer_ticket_selector()

    def get(self, request: Request, pet_kindergarden_id: int, customer_id: int) -> Response:
        """
        유저가 반려동물 유치원 고객 티켓 목록을 조회합니다.
        url: /partners/pet-kindergardens/{pet_kindergarden_id}/customers/{customer_id}/tickets

        Args:
            pet_kindergarden_id (int): 반려동물 유치원 아이디
            customer_id (int): 고객 아이디

        Returns:
            OutputSerializer: 반려동물 유치원 고객 티켓 목록 조회 결과
                id (int): 티켓 아이디
                usage_time_count (int): 사용 가능 시간
                usage_count (int): 사용 가능 횟수
                usage_period_in_days_count (int): 사용 가능 일수
                price (int): 가격
                ticket_type (str): 티켓 타입
                created_at (datetime): 생성 일시
                expired_at (datetime): 만료 일시
                status (str): 상태
        """
        self._pet_kindergarden_selector.check_is_exists_pet_kindergarden_by_id_and_user(
            pet_kindergarten_id=pet_kindergarden_id,
            user=request.user,
        )
        self._customer_selector.check_is_exists_customer_by_id(customer_id=customer_id)
        customer_tickets = self._customer_ticket_selector.get_customer_ticket_with_ticket_queryset_by_customer_id(
            customer_id=customer_id,
        )

        pagination_customer_tickets_data = get_paginated_data(
            pagination_class=self.Pagination,
            serializer_class=self.OutputSerializer,
            queryset=customer_tickets,
            request=request,
            view=self,
        )
        return create_response(data=pagination_customer_tickets_data, status_code=status.HTTP_200_OK)


class CustomerTicketCreateAPI(APIAuthMixin, APIView):
    class InputSerializer(BaseSerializer):
        ticket_id = serializers.IntegerField(required=True)

    class OutputSerializer(BaseSerializer):
        id = serializers.IntegerField()
        total_count = serializers.IntegerField()
        used_count = serializers.IntegerField()
        expired_at = serializers.DateTimeField()
        created_at = serializers.DateTimeField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._customer_ticket_service = CustomerContainer.customer_ticket_service()

    def post(self, request: Request, pet_kindergarden_id: int, customer_id: int) -> Response:
        """
        유저가 반려동물 유치원 고객 티켓을 등록합니다.
        url: /partners/pet-kindergardens/{pet_kindergarden_id}/customers/{customer_id}/tickets

        Args:
            InputSerializer: 반려동물 유치원 고객 티켓 등록
                ticket_id (int): 티켓 아이디
            pet_kindergarden_id (int): 반려동물 유치원 아이디
            customer_id (int): 고객 아이디

        Returns:
            OutputSerializer: 반려동물 유치원 고객 티켓 등록 결과
                id (int): 티켓 아이디
                total_count (int): 총 사용 가능 횟수
                used_count (int): 사용 횟수
                expired_at (datetime): 만료 일시
                created_at (datetime): 생성 일시
        """
        input_serializer = self.InputSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)

        customer_ticket = self._customer_ticket_service.register_ticket(
            customer_id=customer_id,
            pet_kindergarden_id=pet_kindergarden_id,
            user=request.user,
            **input_serializer.validated_data,
        )

        customer_ticket_data = self.OutputSerializer(customer_ticket).data
        return create_response(data=customer_ticket_data, status_code=status.HTTP_201_CREATED)


class CustomerTicketLogListAPI(APIAuthMixin, APIView):
    class Pagination(LimitOffsetPagination):
        default_limit = 10

    class FilterSerializer(BaseSerializer):
        limit = serializers.IntegerField(default=10, min_value=1, max_value=50)
        offset = serializers.IntegerField(default=0, min_value=0)

    class OutputSerializer(BaseSerializer):
        id = serializers.IntegerField()
        ticket_type = serializers.CharField(source="customer_ticket.ticket.ticket_type")
        usage_time_count = serializers.IntegerField(source="customer_ticket.ticket.usage_time_count")
        usage_count = serializers.IntegerField(source="customer_ticket.ticket.usage_count")
        used_count = serializers.IntegerField(source="customer_ticket.used_count")
        unused_count = serializers.SerializerMethodField()
        reserved_at = serializers.DateTimeField()
        updated_reserved_at = serializers.DateTimeField()
        expired_at = serializers.DateTimeField(source="customer_ticket.expired_at")
        # is_attended = serializers.BooleanField() #@TODO: 컬럼 추가

        def get_unused_count(self, obj) -> int:
            return obj.customer_ticket.total_count - obj.customer_ticket.used_count

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._pet_kindergarden_selector = PetKindergardenContainer.pet_kindergarden_selector()
        self._customer_selector = CustomerContainer.customer_selector()
        self._customer_ticket_log_selector = CustomerContainer.customer_ticket_log_selector()

    def get(self, request: Request, pet_kindergarden_id: int, customer_id: int) -> Response:
        """
        유저가 반려동물 유치원 고객 티켓 로그 목록을 조회합니다.
        url: /partners/pet-kindergardens/{pet_kindergarden_id}/customers/{customer_id}/ticket-logs

        Args:
            pet_kindergarden_id (int): 반려동물 유치원 아이디
            customer_id (int): 고객 아이디

        Returns:
            OutputSerializer: 반려동물 유치원 고객 티켓 로그 목록 조회 결과
                id (int): 티켓 로그 아이디
                ticket_type (str): 티켓 타입
                usage_time_count (int): 사용 가능 시간
                usage_count (int): 사용 가능 횟수
                used_count (int): 사용 횟수
                unused_count (int): 사용 가능 횟수
                reserved_at (datetime): 예약 일시
                updated_reserved_at (datetime): 예약 수정 일시
                expired_at (datetime): 만료 일시
                is_attended (bool): 출석 여부
        """
        self._pet_kindergarden_selector.check_is_exists_pet_kindergarden_by_id_and_user(
            pet_kindergarten_id=pet_kindergarden_id,
            user=request.user,
        )
        self._customer_selector.check_is_exists_customer_by_id(customer_id=customer_id)
        customer_ticket_logs = self._customer_ticket_log_selector.get_customer_ticket_log_with_customer_ticket_and_ticket_queryset_by_customer_id_order_by_created_at_desc(
            customer_id=customer_id,
        )

        pagination_customer_ticket_logs_data = get_paginated_data(
            pagination_class=self.Pagination,
            serializer_class=self.OutputSerializer,
            queryset=customer_ticket_logs,
            request=request,
            view=self,
        )
        return create_response(data=pagination_customer_ticket_logs_data, status_code=status.HTTP_200_OK)


class CustomerPetDeleteAPI(APIAuthMixin, APIView):
    class OutputSerializer(BaseSerializer):
        is_possible_delete = serializers.BooleanField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._customer_service = CustomerContainer.customer_service()

    def delete(self, request: Request, pet_kindergarden_id: int, customer_id: int, pet_id: int) -> Response:
        """
        유저가 반려동물 유치원 고객 반려동물을 삭제 가능 여부를 확인합니다.
        url: /partners/pet-kindergardens/{pet_kindergarden_id}/customers/{customer_id}/pets/{pet_id}

        Args:
            pet_kindergarden_id (int): 반려동물 유치원 아이디
            customer_id (int): 고객 아이디
            pet_id (int): 반려동물 아이디

        Returns:
            OutputSerializer: 반려동물 유치원 고객 반려동물 삭제 결과
                is_possible_delete (bool): 삭제 가능 여부
        """
        is_possible_delete = self._customer_service.check_is_possible_delete_customer_pet(
            pet_kindergarden_id=pet_kindergarden_id,
            user=request.user,
            customer_id=customer_id,
            pet_id=pet_id,
        )
        return create_response(data={"is_possible_delete": is_possible_delete}, status_code=status.HTTP_200_OK)
