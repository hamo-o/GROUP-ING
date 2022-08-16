# Generated by Django 4.1 on 2022-08-12 18:06

from django.conf import settings
import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('meetings', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='meetTravelInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year', models.IntegerField()),
                ('month', models.IntegerField()),
                ('day', models.IntegerField()),
                ('meetId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='meetings.meetings', verbose_name='약속 PK')),
                ('meetUsers', models.ManyToManyField(related_name='meetUser', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='meetTravel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('startDate', models.DateTimeField(verbose_name='시작 날짜')),
                ('endDate', models.DateTimeField(verbose_name='종료 날짜')),
                ('meetId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='meetings.meetings', verbose_name='약속 PK')),
                ('userId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='사용자 PK')),
            ],
        ),
        migrations.CreateModel(
            name='meetDayInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year', models.IntegerField()),
                ('month', models.IntegerField()),
                ('day', models.IntegerField()),
                ('hours', django.contrib.postgres.fields.ArrayField(base_field=django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(), size=None), size=24)),
                ('meetId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='meetings.meetings', verbose_name='약속 PK')),
            ],
        ),
        migrations.CreateModel(
            name='meetDay',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('startTime', models.DateTimeField(verbose_name='시작시간')),
                ('endTime', models.DateTimeField(verbose_name='종료시간')),
                ('meetId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='meetings.meetings', verbose_name='약속 PK')),
                ('userId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='사용자 PK')),
            ],
        ),
    ]