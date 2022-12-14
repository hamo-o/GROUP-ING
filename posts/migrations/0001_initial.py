# Generated by Django 4.1 on 2022-08-21 07:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('groups', '0001_initial'),
        ('keywords', '0001_initial'),
        ('meetings', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('logDate', models.DateTimeField(blank=True, null=True)),
                ('logLike', models.IntegerField(default=0)),
                ('places', models.JSONField()),
                ('logTitle', models.CharField(max_length=100)),
                ('logContent', models.TextField()),
                ('openRange', models.CharField(choices=[('비공개', '비공개'), ('그룹공개', '그룹공개'), ('전체공개', '전체공개')], max_length=10)),
                ('createAt', models.DateTimeField(auto_now_add=True)),
                ('updateAt', models.DateTimeField(auto_now=True)),
                ('groupId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='groupId', to='groups.group')),
                ('logKeywords', models.ManyToManyField(blank=True, related_name='logKeywords', to='keywords.keyword')),
                ('meetId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='meetings.meetings')),
                ('meetMembers', models.ManyToManyField(related_name='logMeetMembers', to=settings.AUTH_USER_MODEL)),
                ('userId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'post',
            },
        ),
        migrations.CreateModel(
            name='PostImg',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, upload_to='images')),
                ('logId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='posts.post')),
            ],
        ),
    ]
