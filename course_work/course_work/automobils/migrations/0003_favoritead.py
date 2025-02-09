# Generated by Django 5.0.6 on 2024-06-14 05:00

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('automobils', '0002_alter_announcement_date_alter_announcement_image'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='FavoriteAd',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_added', models.DateTimeField(default=django.utils.timezone.now)),
                ('announcement', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='automobils.announcement')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('user', 'announcement')},
            },
        ),
    ]
