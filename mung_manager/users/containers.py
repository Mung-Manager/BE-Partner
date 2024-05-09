from dependency_injector import containers, providers

from mung_manager.users.selectors.users import UserSelector
from mung_manager.users.services.users import UserService


class UserContainer(containers.DeclarativeContainer):
    """이 클래스는 DI(Dependency Injection) 유저 컨테이너 입니다.

    Attributes:
        user_selector: 유저 셀렉터
        user_service: 유저 서비스
    """

    user_selector = providers.Factory(UserSelector)
    user_service = providers.Factory(
        UserService,
        user_selector=user_selector,
    )
