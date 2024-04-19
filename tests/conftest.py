from datetime import datetime

import pytest
from rest_framework.test import APIClient

from mung_manager.users.enums import AuthGroup
from tests.factories import (
    GroupFactory,
    PetKindergardenFactory,
    RawPetKindergardenFactory,
    TicketFactory,
    UserFactory,
    UserSocialProviderFactory,
)


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user_social_provider(db):
    return UserSocialProviderFactory.create_batch(2)


@pytest.fixture
def group(db):
    return GroupFactory.create_batch(4)


@pytest.fixture
def active_partner_user(db, group):
    return UserFactory(
        is_deleted=False,
        is_admin=False,
        is_active=True,
        groups=[AuthGroup.PARTNER.value],
    )


@pytest.fixture
def inactive_partner_user(db, group):
    return UserFactory(
        is_deleted=False,
        is_admin=False,
        is_active=False,
        groups=[AuthGroup.PARTNER.value],
    )


@pytest.fixture
def deleted_partner_user(db, group):
    return UserFactory(
        is_deleted=True,
        deleted_at=datetime.now(),
        is_admin=False,
        is_active=True,
        groups=[AuthGroup.PARTNER.value],
    )


@pytest.fixture
def active_guest_user(db, group):
    return UserFactory(
        is_deleted=False,
        is_admin=False,
        is_active=True,
        groups=[AuthGroup.GUEST.value],
    )


@pytest.fixture
def pet_kindergarden(db, active_partner_user):
    return PetKindergardenFactory(user=active_partner_user)


@pytest.fixture
def raw_pet_kindergarden(db):
    return RawPetKindergardenFactory()


@pytest.fixture
def ticket(db, pet_kindergarden):
    return TicketFactory(pet_kindergarden=pet_kindergarden)
