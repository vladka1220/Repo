# Generated by Django 5.1 on 2024-10-27 11:38

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('service_friends', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='favoriteuser',
            name='favorite',
            field=models.UUIDField(default=uuid.uuid4),
        ),
        migrations.AlterField(
            model_name='favoriteuser',
            name='user',
            field=models.UUIDField(default=uuid.uuid4),
        ),
        migrations.AlterField(
            model_name='friend',
            name='friend',
            field=models.UUIDField(default=uuid.uuid4),
        ),
        migrations.AlterField(
            model_name='friend',
            name='user',
            field=models.UUIDField(default=uuid.uuid4),
        ),
        migrations.AlterField(
            model_name='friendrequest',
            name='from_user',
            field=models.UUIDField(default=uuid.uuid4),
        ),
        migrations.AlterField(
            model_name='friendrequest',
            name='to_user',
            field=models.UUIDField(default=uuid.uuid4),
        ),
    ]
