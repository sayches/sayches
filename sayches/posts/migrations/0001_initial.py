# Generated by Django 3.2.13 on 2022-05-30 01:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import utils.upload_path


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='BlacklistWords',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('word', models.CharField(blank=True, max_length=140, null=True, unique=True)),
                ('is_emoji', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name_plural': 'Blacklist Words',
            },
        ),
        migrations.CreateModel(
            name='LinkValidation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('url', models.URLField(blank=True, null=True, unique=True)),
                ('type', models.CharField(choices=[('1', 'Adult Website'), ('2', 'Suspicious Website')], default='2', max_length=2)),
                ('default_message', models.CharField(choices=[(' ', ' No default message '), (' The terms of service raise very serious concerns.  ', 'The terms of service raise very serious concerns '), (' WARNING: This website has been blacklisted. ', 'WARNING: This website has been blacklisted ')], default=' ', max_length=100, null=True)),
                ('customized_message', models.TextField(blank=True, max_length=300, null=True)),
            ],
            options={
                'verbose_name_plural': 'Links Blacklist',
            },
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('id', models.CharField(editable=False, max_length=10, primary_key=True, serialize=False)),
                ('text', models.TextField(null=True)),
                ('have_mentions', models.BooleanField(default=False)),
                ('flair', models.CharField(choices=[('No Flair', 'No Flair'), ('Leak', 'Leak'), ('SOS', 'SOS')], max_length=50, null=True)),
                ('post_option', models.CharField(choices=[('normal', 'normal'), ('media', 'media')], max_length=50, null=True)),
                ('pinned_post', models.BooleanField(default=False)),
                ('media', models.FileField(blank=True, null=True, upload_to=utils.upload_path.uuid_media)),
                ('restrict', models.BooleanField(blank=True, null=True)),
                ('post_followers', models.ManyToManyField(blank=True, related_name='post_followed', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='posts', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-created_at',),
            },
        ),
        migrations.CreateModel(
            name='ReportPost',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('post_text', models.TextField(blank=True, null=True)),
                ('post_url', models.CharField(blank=True, max_length=100, null=True)),
                ('complaint_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('removal_date', models.DateTimeField(blank=True, null=True)),
                ('flagging_reason', models.CharField(max_length=500)),
                ('flagger_type', models.CharField(blank=True, choices=[('', ''), ('Automated flagging', 'Automated flagging'), ('Government agency', 'Government agency'), ('Individual trusted flagger', 'Individual trusted flagger'), ('NGO', 'NGO'), ('User', 'User')], default='', max_length=500, null=True)),
                ('outcome', models.CharField(blank=True, choices=[('', ''), ('Account has been suspended', 'Account has been suspended'), ('No action taken', 'No action taken'), ('Post was removed', 'Post was removed')], default='', max_length=500, null=True)),
                ('appeal', models.CharField(blank=True, choices=[('', ''), ('Reversed', 'Reversed'), ('Upheld', 'Upheld')], default='', max_length=100, null=True)),
                ('notes', models.TextField(blank=True, null=True)),
                ('post_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='posts.post')),
                ('post_reporter', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='post_reporter', to=settings.AUTH_USER_MODEL)),
                ('post_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='post_user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Reported Posts',
            },
        ),
        migrations.CreateModel(
            name='PostsTimestamp',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('post_id', models.CharField(blank=True, max_length=10, null=True)),
                ('post_timestamp', models.DateTimeField(blank=True, null=True)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Posts Timestamp',
            },
        ),
        migrations.CreateModel(
            name='Mentions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('explicit_name', models.CharField(blank=True, max_length=255)),
                ('implicit_name', models.CharField(blank=True, max_length=255)),
                ('posts', models.ManyToManyField(related_name='mentions', to='posts.Post')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Likes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('reaction_name', models.CharField(blank=True, max_length=25, null=True)),
                ('post', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='post_likes', to='posts.post')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_likes', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Likes',
            },
        ),
        migrations.CreateModel(
            name='Hashtag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('explicit_name', models.CharField(blank=True, max_length=255)),
                ('implicit_name', models.CharField(blank=True, max_length=255)),
                ('hashtag_counter', models.PositiveIntegerField(default=1)),
                ('status', models.IntegerField(choices=[(0, 'Clean'), (1, 'Propaganda')], default=0, verbose_name='status')),
                ('author', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('posts', models.ManyToManyField(related_name='hashtags', to='posts.Post')),
            ],
            options={
                'ordering': ('-hashtag_counter',),
            },
        ),
    ]
