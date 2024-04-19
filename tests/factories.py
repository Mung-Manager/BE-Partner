import json
from datetime import datetime

import factory
import pytz
from django.contrib.auth.models import Group
from factory.fuzzy import FuzzyChoice, FuzzyDate, FuzzyDateTime, FuzzyInteger
from faker import Faker

from mung_manager.pet_kindergardens.enums import (
    ReservationAvailabilityOption,
    ReservationChangeOption,
)
from mung_manager.pet_kindergardens.models import PetKindergarden, RawPetKindergarden
from mung_manager.tickets.enums import TicketType
from mung_manager.tickets.models import Ticket
from mung_manager.users.models import User, UserSocialProvider

faker = Faker("ko_KR")


class UserSocialProviderFactory(factory.django.DjangoModelFactory):
    id = factory.Iterator(range(1, 3))
    name = factory.Iterator(["email", "kakao"])
    description = factory.Iterator(["이메일", "카카오"])

    class Meta:
        model = UserSocialProvider


class GroupFactory(factory.django.DjangoModelFactory):
    id = factory.Iterator(range(1, 5))
    name = factory.Iterator(["admin", "superuser", "guest", "partner"])

    class Meta:
        model = Group


class UserFactory(factory.django.DjangoModelFactory):
    email = factory.LazyAttribute(lambda _: faker.unique.email())
    social_id = factory.LazyAttribute(lambda _: faker.unique.uuid4())
    password = factory.LazyAttribute(lambda _: faker.password())
    name = factory.LazyAttribute(lambda _: faker.name())
    gender = FuzzyChoice(choices=["M", "F"])
    birth = FuzzyDate(start_date=datetime(1990, 1, 1), end_date=datetime(2000, 12, 31))
    phone_number = factory.LazyAttribute(lambda _: faker.unique.phone_number())
    is_agree_privacy = True
    is_agree_marketing = factory.LazyAttribute(lambda _: faker.boolean())
    last_login = FuzzyDateTime(start_dt=datetime(2021, 1, 1, tzinfo=pytz.utc))
    user_social_provider = factory.SubFactory(UserSocialProviderFactory)

    class Meta:
        model = User

    @factory.post_generation
    def deleted_at(self, create, extracted, **kwargs):
        if isinstance(extracted, datetime):
            self.deleted_at = extracted
        else:
            self.deleted_at = None

    @factory.post_generation
    def is_deleted(self, create, extracted, **kwargs):
        if isinstance(extracted, bool):
            self.is_deleted = extracted
        else:
            self.is_deleted = False

    @factory.post_generation
    def is_admin(self, create, extracted, **kwargs):
        if isinstance(extracted, bool):
            self.is_admin = extracted
        else:
            self.is_admin = False

    @factory.post_generation
    def is_superuser(self, create, extracted, **kwargs):
        if isinstance(extracted, bool):
            self.is_superuser = extracted
        else:
            self.is_superuser = False

    @factory.post_generation
    def is_active(self, create, extracted, **kwargs):
        if isinstance(extracted, bool):
            self.is_active = extracted
        else:
            self.is_active = True

    @factory.post_generation
    def groups(self, create, extracted, **kwargs):
        if extracted:
            for group in extracted:
                self.groups.add(group)


class PetKindergardenFactory(factory.django.DjangoModelFactory):
    name = factory.LazyAttribute(lambda _: faker.unique.company())
    main_thumbnail_url = factory.LazyAttribute(lambda _: faker.unique.image_url())
    profile_thumbnail_url = factory.LazyAttribute(lambda _: faker.unique.image_url())
    phone_number = factory.LazyAttribute(lambda _: faker.unique.phone_number())
    visible_phone_number = factory.LazyAttribute(lambda _: [faker.unique.phone_number() for _ in range(2)])
    business_hours = FuzzyChoice(choices=["09:00 ~ 06:00", "10:00 ~ 07:00", "11:00 ~ 08:00"])
    road_address = factory.LazyAttribute(lambda _: faker.address())
    abbr_address = factory.LazyAttribute(lambda _: faker.address())
    detail_address = factory.LazyAttribute(lambda _: faker.address())
    short_address = factory.LazyAttribute(lambda _: [faker.address() for _ in range(10)])
    guide_message = factory.LazyAttribute(lambda _: faker.text())
    latitude = factory.LazyAttribute(lambda _: faker.latitude())
    longitude = factory.LazyAttribute(lambda _: faker.longitude())
    point = factory.LazyAttribute(
        lambda _: json.dumps(
            {
                "type": "Point",
                "coordinates": [float(faker.longitude()), float(faker.latitude())],
            }
        )
    )
    reservation_availability_option = FuzzyChoice(choices=[e.value for e in ReservationAvailabilityOption])
    reservation_change_option = FuzzyChoice(choices=[e.value for e in ReservationChangeOption])
    daily_pet_limit = factory.LazyAttribute(lambda _: faker.random_int(min=1, max=100))
    user = factory.SubFactory(UserFactory)

    class Meta:
        model = PetKindergarden


class RawPetKindergardenFactory(factory.django.DjangoModelFactory):
    thum_url = factory.LazyAttribute(lambda _: faker.unique.image_url())
    tel = factory.LazyAttribute(lambda _: faker.unique.phone_number())
    virtual_tel = factory.LazyAttribute(lambda _: faker.unique.phone_number())
    name = factory.LazyAttribute(lambda _: faker.unique.company())
    x = factory.LazyAttribute(lambda _: faker.longitude())
    y = factory.LazyAttribute(lambda _: faker.latitude())
    business_hours = FuzzyChoice(choices=["09:00 ~ 06:00", "10:00 ~ 07:00", "11:00 ~ 08:00"])
    address = factory.LazyAttribute(lambda _: faker.address())
    road_address = factory.LazyAttribute(lambda _: faker.address())
    abbr_address = factory.LazyAttribute(lambda _: faker.address())
    short_address = factory.LazyAttribute(lambda _: [faker.address() for _ in range(10)])

    class Meta:
        model = RawPetKindergarden


class TicketFactory(factory.django.DjangoModelFactory):
    usage_time_count = FuzzyInteger(1, 24)
    usage_count = FuzzyInteger(1, 100)
    usage_period_in_days_count = FuzzyInteger(1, 30)
    price = FuzzyInteger(1000, 100000)
    ticket_type = FuzzyChoice(choices=[e.value for e in TicketType])
    pet_kindergarden = factory.SubFactory(PetKindergardenFactory)

    class Meta:
        model = Ticket

    @factory.post_generation
    def is_deleted(self, create, extracted, **kwargs):
        if isinstance(extracted, bool):
            self.is_deleted = extracted
        else:
            self.is_deleted = False

    @factory.post_generation
    def deleted_at(self, create, extracted, **kwargs):
        if isinstance(extracted, datetime):
            self.deleted_at = extracted
        else:
            self.deleted_at = None
