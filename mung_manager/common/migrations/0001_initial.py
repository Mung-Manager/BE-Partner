# Generated by Django 4.2.11 on 2024-04-07 22:59

import uuid

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DeletedRecord',
            fields=[
                ('id', models.UUIDField(db_comment='삭제된 레코드 아이디', default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('original_table', models.CharField(db_comment='원본 테이블', max_length=256)),
                ('original_id', models.IntegerField(db_comment='원본 아이디')),
                ('data', models.JSONField(db_comment='원본 데이터')),
                ('deleted_at', models.DateTimeField(auto_now_add=True, db_comment='삭제 시간')),
            ],
            options={
                'db_table': 'deleted_record',
            },
        ),
    ]
