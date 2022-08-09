# Generated by Django 4.1 on 2022-08-06 14:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('groups', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Meetings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('meetHead', models.CharField(max_length=100)),
                ('meetName', models.CharField(max_length=100)),
                ('meetTime', models.DateField()),
                ('meetPlace', models.CharField(max_length=100)),
                ('meetStatus', models.IntegerField(default=0)),
                ('meetStart', models.DateField()),
                ('meetEnd', models.DateField()),
                ('meetVote', models.IntegerField(default=0)),
                ('meetMembers', models.IntegerField(default=0)),
                ('meetGroupId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='groups.group')),
            ],
        ),
    ]
