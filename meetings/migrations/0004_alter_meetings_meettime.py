# Generated by Django 4.1 on 2022-08-12 05:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meetings', '0003_alter_meetings_meettime'),
    ]

    operations = [
        migrations.AlterField(
            model_name='meetings',
            name='meetTime',
            field=models.DateField(null=True),
        ),
    ]
