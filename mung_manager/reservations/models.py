from django.db import models

from mung_manager.common.base.models import TimeStampedModel


class Reservation(TimeStampedModel):
    id = models.AutoField(auto_created=True, primary_key=True, db_column="reservation_id", serialize=False, db_comment="예약 아이디")
    is_attended = models.BooleanField(db_comment="출석 여부", null=True)
    reserved_at = models.DateTimeField(db_comment="예약 시간")
    updated_reserved_at = models.DateTimeField(db_comment="예약 수정 시간", null=True)
    attendance_time = models.TimeField(db_comment="출석 시간")
    is_cancelled = models.BooleanField(db_comment="취소 여부", default=False)
    customer = models.ForeignKey(
        "customers.Customer",
        on_delete=models.CASCADE,
        related_name="reservations",
        db_comment="고객 아이디",
    )
    customer_pet = models.ForeignKey(
        "customers.CustomerPet",
        on_delete=models.CASCADE,
        related_name="reservations",
        db_comment="고객 펫 아이디",
    )
    customer_ticket = models.ForeignKey(
        "customers.CustomerTicket",
        on_delete=models.CASCADE,
        related_name="reservations",
        db_comment="고객 티켓 아이디",
    )
    pet_kindergarden = models.ForeignKey(
        "pet_kindergardens.PetKindergarden",
        on_delete=models.CASCADE,
        related_name="reservations",
        db_comment="펫 유치원 아이디",
    )

    def __str__(self):
        return f"[{self.id}]: {self.customer.name} - {self.pet_kindergarden.name}"

    class Meta:
        db_table = "reservation"


class DailyReservation(TimeStampedModel):
    id = models.AutoField(auto_created=True, primary_key=True, db_column="daily_reservation_id", serialize=False, db_comment="일일 예약 아이디")
    reserved_at = models.DateField(db_comment="예약 날짜")
    total_pet_count = models.SmallIntegerField(db_comment="총 반려동물 수", default=0)
    time_pet_count = models.SmallIntegerField(db_comment="시간권 반려동물 수", default=0)
    all_day_pet_count = models.SmallIntegerField(db_comment="종일권 반려동물 수", default=0)
    hotel_pet_count = models.SmallIntegerField(db_comment="호텔 반려동물 수", default=0)

    def __str__(self):
        return f"[{self.id}]: {self.reserved_at}"

    class Meta:
        db_table = "daily_reservation"
