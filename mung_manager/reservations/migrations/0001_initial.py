# Generated by Django 5.0.4 on 2024-05-07 08:06

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('customers', '0001_initial'),
        ('pet_kindergardens', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='DailyReservation',
            fields=[
                ('id', models.AutoField(auto_created=True, db_column='daily_reservation_id', db_comment='일일 예약 아이디', primary_key=True, serialize=False)),
                ('reserved_at', models.DateField(db_comment='예약 날짜')),
                ('total_pet_count', models.SmallIntegerField(db_comment='총 반려동물 수', default=0)),
                ('time_pet_count', models.SmallIntegerField(db_comment='시간권 반려동물 수', default=0)),
                ('all_day_pet_count', models.SmallIntegerField(db_comment='종일권 반려동물 수', default=0)),
                ('hotel_pet_count', models.SmallIntegerField(db_comment='호텔 반려동물 수', default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True, db_comment='생성 일시')),
                ('updated_at', models.DateTimeField(auto_now=True, db_comment='수정 일시')),
            ],
            options={
                'db_table': 'daily_reservation',
            },
        ),
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('id', models.AutoField(auto_created=True, db_column='reservation_id', db_comment='예약 아이디', primary_key=True, serialize=False)),
                ('is_attended', models.BooleanField(db_comment='출석 여부', null=True)),
                ('reserved_at', models.DateTimeField(db_comment='예약 시간')),
                ("end_at", models.DateTimeField(db_comment="퇴실 시간", null=True)),
                ('reservation_status', models.CharField(choices=[('완료', 'COMPLETED'), ('취소', 'CANCELED'), ('변경', 'MODIFIED')], db_comment='예약 상태', max_length=8)),
                ('created_at', models.DateTimeField(auto_now_add=True, db_comment='생성 일시')),
                ('updated_at', models.DateTimeField(auto_now=True, db_comment='수정 일시')),
                ('depth', models.PositiveIntegerField(db_comment='노드 깊이', default=0)),
                ('parent', models.ForeignKey(db_comment='부모 예약 아이디', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='reservations.reservation')),
                ('customer', models.ForeignKey(db_comment='고객 아이디', on_delete=django.db.models.deletion.CASCADE, related_name='reservations', to='customers.customer')),
                ('customer_pet', models.ForeignKey(db_comment='고객 펫 아이디', on_delete=django.db.models.deletion.CASCADE, related_name='reservations', to='customers.customerpet')),
                ('customer_ticket', models.ForeignKey(db_comment='고객 티켓 아이디', on_delete=django.db.models.deletion.CASCADE, related_name='reservations', to='customers.customerticket')),
                ('pet_kindergarden', models.ForeignKey(db_comment='펫 유치원 아이디', on_delete=django.db.models.deletion.CASCADE, related_name='reservations', to='pet_kindergardens.petkindergarden')),
            ],
            options={
                'db_table': 'reservation',
            },
        ),
        migrations.CreateModel(
            name='DayOff',
            fields=[
                ('id', models.AutoField(auto_created=True, db_column='day_off_id', db_comment='휴무 아이디', primary_key=True, serialize=False)),
                ('day_off_at', models.DateField(db_comment='휴무 날짜')),
                ('created_at', models.DateTimeField(auto_now_add=True, db_comment='생성 일시')),
                ('updated_at', models.DateTimeField(auto_now=True, db_comment='수정 일시')),
                ('pet_kindergarden', models.ForeignKey(db_comment='펫 유치원 아이디', on_delete=django.db.models.deletion.CASCADE, related_name='day_offs', to='pet_kindergardens.petkindergarden')),
            ],
            options={
                'db_table': 'day_off',
            },
        ),
        migrations.CreateModel(
            name='KoreaSpecialDay',
            fields=[
                ('id', models.AutoField(auto_created=True, db_column='korea_special_day_id', db_comment='한국 공휴일 아이디', primary_key=True, serialize=False)),
                ('name', models.CharField(db_comment='공휴일 이름', max_length=64)),
                ('special_day_at', models.DateField(db_comment='공휴일 날짜')),
                ('is_holiday', models.BooleanField(db_comment='공휴일 여부', default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, db_comment='생성 일시')),
                ('updated_at', models.DateTimeField(auto_now=True, db_comment='수정 일시')),
            ],
            options={
                'db_table': 'korea_special_day',
            },
        ),
    ]
