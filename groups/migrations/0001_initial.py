# Generated by Django 4.1 on 2022-08-19 05:46

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=40, verbose_name='그룹명')),
                ('head', models.CharField(max_length=20, verbose_name='그룹장')),
                ('code', models.CharField(max_length=30, verbose_name='그룹 코드')),
                ('introduction', models.TextField(blank=True, null=True, verbose_name='그룹 소개')),
                ('purpose', models.TextField(blank=True, null=True, verbose_name='그룹 목적')),
                ('image', models.ImageField(blank=True, null=True, upload_to='groups/%Y%m%d', verbose_name='그룹 대표사진')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
