# Generated by Django 4.1 on 2022-08-18 11:58

from django.db import migrations, models
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('email', models.EmailField(max_length=255, unique=True, verbose_name='이메일')),
                ('username', models.CharField(max_length=20, unique=True)),
                ('name', models.CharField(max_length=20, verbose_name='이름')),
                ('nickname', models.CharField(max_length=20, null=True, unique=True, verbose_name='닉네임')),
                ('age', models.IntegerField(null=True, verbose_name='나이')),
                ('profileImg', models.ImageField(blank=True, null=True, upload_to='logins/%Y%m%d', verbose_name='프로필사진')),
                ('phoneNumber', phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None, unique=True, verbose_name='전화번호')),
                ('address', models.CharField(max_length=100, verbose_name='주소')),
                ('addressDetail', models.CharField(max_length=100, verbose_name='상세주소')),
                ('gender', models.CharField(choices=[('남성', '남성'), ('여성', '여성'), ('선택안함', '선택안함')], max_length=10, verbose_name='성별')),
                ('intro', models.CharField(blank=True, default='안녕하세요. 반가워요', max_length=100, null=True, verbose_name='한줄소개')),
                ('auth', models.CharField(max_length=10, null=True, verbose_name='인증번호')),
                ('is_active', models.BooleanField(default=False)),
                ('is_admin', models.BooleanField(default=False)),
                ('is_superuser', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
