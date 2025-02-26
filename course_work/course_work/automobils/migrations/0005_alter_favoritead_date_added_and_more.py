# Generated by Django 5.1.4 on 2025-01-10 05:35

import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('automobils', '0004_alter_favoritead_unique_together_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='favoritead',
            name='date_added',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterUniqueTogether(
            name='favoritead',
            unique_together={('user', 'announcement')},
        ),
    ]
