from django.contrib.gis.db.models import PointField
from django.contrib.postgres.fields import ArrayField
from django.db import models

from mung_manager.common.base.models import TimeStampedModel
from mung_manager.pet_kindergardens.enums import (
    ReservationAvailabilityOption,
    ReservationChangeOption,
)
from mung_manager.users.models import User


class PetKindergarden(TimeStampedModel):
    id = models.AutoField(auto_created=True, primary_key=True, db_column="pet_kindergarden_id", serialize=False, db_comment="펫 유치원 아이디")
    name = models.CharField(max_length=64, db_comment="유치원 이름")
    main_thumbnail_url = models.URLField(db_comment="메인 썸네일")
    profile_thumbnail_url = models.URLField(db_comment="프로필 썸네일 이미지")
    phone_number = models.CharField(max_length=16, db_comment="전화번호", blank=True)
    visible_phone_number = ArrayField(models.CharField(max_length=16), db_comment="노출 전화번호", size=2)
    business_hours = models.CharField(max_length=64, db_comment="영업 시간")
    road_address = models.CharField(max_length=128, db_comment="도로명 주소")
    abbr_address = models.CharField(max_length=128, db_comment="지번 주소")
    detail_address = models.CharField(max_length=128, db_comment="상세 주소", blank=True)
    short_address = ArrayField(models.CharField(max_length=128), db_comment="간단 주소", size=10)
    guide_message = models.TextField(db_comment="안내 메시지", blank=True)
    latitude = models.DecimalField(max_digits=8, decimal_places=6, db_comment="위도")
    longitude = models.DecimalField(max_digits=9, decimal_places=6, db_comment="경도")
    point = PointField(db_comment="위치 좌표")
    reservation_availability_option = models.CharField(
        max_length=64, db_comment="예약 가능 설정", choices=[(o.value, o.name) for o in ReservationAvailabilityOption]
    )
    reservation_change_option = models.CharField(
        max_length=64, db_comment="예약 변경 설정", choices=[(o.value, o.name) for o in ReservationChangeOption]
    )
    daily_pet_limit = models.SmallIntegerField(db_comment="일일 펫 제한")
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="pet_kindergardens",
        db_comment="유저 아이디",
    )

    def __str__(self):
        return f"[{self.id}]: {self.name}"

    class Meta:
        db_table = "pet_kindergarden"


class RawPetKindergarden(models.Model):
    """
    반려동물 유치원 raw 데이터 (네이버 지도 데이터)
    """

    id = models.AutoField(auto_created=True, primary_key=True, serialize=False, db_comment="펫 유치원 로우 아이디")
    thum_url = models.URLField(db_column="thumUrl", db_comment="썸네일 이미지")
    tel = models.CharField(max_length=16, db_column="tel", db_comment="전화번호")
    virtual_tel = models.CharField(max_length=16, blank=True, db_column="virtualTel", db_comment="가상 전화번호")
    name = models.CharField(max_length=64, db_column="name", db_comment="이름")
    x = models.DecimalField(max_digits=9, decimal_places=6, db_column="x", db_comment="경도")
    y = models.DecimalField(max_digits=8, decimal_places=6, db_column="y", db_comment="위도")
    business_hours = models.CharField(max_length=64, db_column="businessHours", db_comment="영업 시간")
    address = models.CharField(max_length=128, db_column="address", db_comment="주소")
    road_address = models.CharField(max_length=128, db_column="roadAddress", db_comment="도로명 주소")
    abbr_address = models.CharField(max_length=128, db_column="abbrAddress", db_comment="지번 주소")
    short_address = ArrayField(models.CharField(max_length=128), size=10, db_column="shortAddress", db_comment="간단 주소")

    def __str__(self):
        return f"[{self.id}]: {self.name}"

    class Meta:
        db_table = "raw_pet_kindergarden"


class DayOff(TimeStampedModel):
    id = models.AutoField(auto_created=True, primary_key=True, db_column="day_off_id", serialize=False, db_comment="휴무 아이디")
    day_off_at = models.DateField(db_comment="휴무 날짜")
    pet_kindergarden = models.ForeignKey(
        PetKindergarden,
        on_delete=models.CASCADE,
        related_name="day_offs",
        db_comment="펫 유치원 아이디",
    )

    def __str__(self):
        return f"[{self.id}]: {self.pet_kindergarden.name} - {self.day_off}"

    class Meta:
        db_table = "day_off"


class KoreaSpecialDay(TimeStampedModel):
    id = models.AutoField(auto_created=True, primary_key=True, db_column="korea_special_day_id", serialize=False, db_comment="한국 공휴일 아이디")
    name = models.CharField(max_length=64, db_comment="공휴일 이름")
    special_day_at = models.DateField(db_comment="공휴일 날짜")

    def __str__(self):
        return f"[{self.id}]: {self.name} - {self.special_day_at}"

    class Meta:
        db_table = "korea_special_day"
