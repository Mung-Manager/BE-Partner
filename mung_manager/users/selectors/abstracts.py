from abc import ABC, abstractmethod
from typing import Optional

from mung_manager.errors.exceptions import NotImplementedException
from mung_manager.users.models import User


class AbstractUserSelector(ABC):
    @abstractmethod
    def get_by_social_id(self, social_id: str) -> Optional[User]:
        raise NotImplementedException()

    @abstractmethod
    def exists_by_email_excluding_self(
        self,
        user,
        email: Optional[str] = None,
    ) -> bool:
        raise NotImplementedException()


class AbstractGroupSelector(ABC):
    @abstractmethod
    def exists_by_id_and_user(self, group_id: int, user) -> bool:
        raise NotImplementedException()
