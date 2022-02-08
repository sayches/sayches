# Generated by Django 3.2.9 on 2022-02-08 13:52

from django.conf import settings
import django.contrib.auth.validators
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import django_countries.fields
import sayches.utils.upload_path
import users.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('name', models.CharField(blank=True, max_length=49, verbose_name='Name of User')),
                ('user_hash', models.CharField(max_length=15, null=True, unique=True, validators=[django.core.validators.RegexValidator(code='invalid_username', message='Username must be Alphanumeric only', regex='^@[ء-يa-zA-Z\\d\\-_\\s]+$')])),
                ('country', django_countries.fields.CountryField(blank=True, max_length=2, null=True)),
                ('first_login', models.BooleanField(default=False)),
                ('first_post', models.BooleanField(default=False)),
                ('lost_virginity', models.BooleanField(default=False)),
                ('profile_update_time', models.IntegerField(choices=[(24, '24'), (48, '48'), (72, '72'), (0, '0')], default=0)),
                ('warrant_canary', models.BooleanField(default=True)),
                ('alias', models.CharField(choices=[('Unknown', 'Unknown'), ('Unidentified', 'Unidentified'), ('Anonymous', 'Anonymous'), ('Nameless', 'Nameless')], default='Anonymous', max_length=20)),
                ('notes', models.TextField(blank=True, null=True)),
                ('auto_account_delete_time', models.IntegerField(choices=[(0, 'DISPOSABLE'), (1, '1'), (6, '6'), (12, '12')], default=12)),
                ('last_activity_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('send_email', models.BooleanField(blank=True, null=True)),
                ('disposable', models.BooleanField(blank=True, default=False, null=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', users.models.CustomUserManager()),
            ],
        ),
        migrations.CreateModel(
            name='CannedResponse',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('message', models.TextField(null=True)),
            ],
            options={
                'verbose_name_plural': 'Canned Response',
                'ordering': ('-created_at',),
            },
        ),
        migrations.CreateModel(
            name='DeletedUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('user_hash', models.CharField(max_length=15, null=True)),
                ('country', django_countries.fields.CountryField(max_length=2, null=True)),
                ('warrant_canary', models.BooleanField(default=True)),
                ('profile_update_time', models.IntegerField(choices=[(24, '24'), (48, '48'), (72, '72'), (0, '0')], default=24)),
                ('auto_account_delete_time', models.IntegerField(choices=[(0, 'DISPOSABLE'), (1, '1'), (6, '6'), (12, '12')], default=12)),
                ('last_activity_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now)),
                ('deleted_date_time', models.DateTimeField(auto_now_add=True, null=True)),
                ('bio', models.CharField(blank=True, max_length=150, null=True)),
                ('pgp_fingerprint', models.CharField(blank=True, max_length=49, null=True)),
                ('btc_address', models.CharField(blank=True, max_length=45, null=True)),
                ('website', models.URLField(blank=True, null=True)),
                ('disposable', models.BooleanField(null=True)),
                ('notes', models.TextField(null=True)),
                ('alias', models.CharField(max_length=20, null=True)),
                ('lost_virginity', models.BooleanField(null=True)),
                ('first_post', models.BooleanField(null=True)),
                ('first_login', models.BooleanField(null=True)),
            ],
            options={
                'verbose_name_plural': 'Deleted Users',
            },
        ),
        migrations.CreateModel(
            name='PreUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('name', models.CharField(max_length=100, null=True)),
                ('email', models.EmailField(max_length=100, null=True)),
                ('is_added_by_admin', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name_plural': 'Pre Users',
            },
        ),
        migrations.CreateModel(
            name='UserStatistics',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('date', models.DateField(default=django.utils.timezone.now)),
                ('total_users', models.IntegerField(default=0)),
                ('total_active_users', models.IntegerField(default=0)),
                ('total_inactive_users', models.IntegerField(default=0)),
                ('total_verified_users', models.IntegerField(default=0)),
                ('total_deleted_user', models.IntegerField(default=0)),
            ],
            options={
                'verbose_name_plural': 'Statistics',
            },
        ),
        migrations.CreateModel(
            name='UserVerification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('url', models.URLField(null=True)),
                ('verification', models.CharField(blank=True, choices=[('Fraudulent', 'Fraudulent'), ('Bot', 'Bot'), ('Official', 'Official'), ('Verified', 'Verified')], max_length=100, null=True)),
                ('verified', models.BooleanField(default=False)),
                ('application_status', models.CharField(blank=True, choices=[('Approved', 'Approved'), ('Rejected', 'Rejected'), ('Removed', 'Removed')], max_length=100, null=True)),
                ('user', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Verifications',
            },
        ),
        migrations.CreateModel(
            name='UserRSA',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('public_pem', models.TextField(blank=True, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'User RSA',
            },
        ),
        migrations.CreateModel(
            name='SendEmail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('_from', models.CharField(choices=[('info@sayches.com', 'info@sayches.com')], max_length=100)),
                ('_to', models.EmailField(max_length=254, null=True)),
                ('_subject', models.CharField(max_length=250)),
                ('_message', models.TextField(blank=True)),
                ('_passcode', models.CharField(max_length=20, null=True)),
                ('_canned_response', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='users.cannedresponse')),
            ],
            options={
                'verbose_name_plural': 'Send Email',
                'ordering': ('-created_at',),
            },
        ),
        migrations.CreateModel(
            name='ReportUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('complaint_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('removal_date', models.DateTimeField(blank=True, null=True)),
                ('flagging_reason', models.CharField(max_length=500)),
                ('flagger_type', models.CharField(blank=True, choices=[('', ''), ('Automated flagging', 'Automated flagging'), ('Government agency', 'Government agency'), ('Individual trusted flagger', 'Individual trusted flagger'), ('NGO', 'NGO'), ('User', 'User')], default='', max_length=500, null=True)),
                ('outcome', models.CharField(blank=True, choices=[('', ''), ('Account has been suspended', 'Account has been suspended'), ('No action taken', 'No action taken'), ('Post was removed', 'Post was removed')], default='', max_length=500, null=True)),
                ('appeal', models.CharField(blank=True, choices=[('', ''), ('Reversed', 'Reversed'), ('Upheld', 'Upheld')], default='', max_length=100, null=True)),
                ('notes', models.TextField(blank=True, null=True)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='user', to=settings.AUTH_USER_MODEL)),
                ('user_reporter', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='user_reporter', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Reported Users',
            },
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('photo', models.ImageField(blank=True, null=True, upload_to=sayches.utils.upload_path.uuid_profilepicture)),
                ('bio', models.CharField(blank=True, max_length=150)),
                ('pgp_fingerprint', models.CharField(blank=True, max_length=49, null=True)),
                ('btc_address', models.CharField(blank=True, max_length=42, null=True)),
                ('website', models.URLField(blank=True, max_length=70, null=True)),
                ('disable_notifications', models.BooleanField(default=False)),
                ('disable_messages', models.BooleanField(default=False)),
                ('disable_ping', models.BooleanField(default=False)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PingPong',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('pong', models.BooleanField(default=False)),
                ('pong_time', models.DateTimeField(blank=True, null=True)),
                ('pinged_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pinged', to=settings.AUTH_USER_MODEL)),
                ('pinger_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pinger', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-created_at',),
            },
        ),
        migrations.CreateModel(
            name='LoggedInUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('session_key', models.CharField(blank=True, max_length=32, null=True)),
                ('user', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='logged_in_user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Logged In User',
            },
        ),
        migrations.CreateModel(
            name='FromSayches',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('title', models.CharField(blank=True, max_length=100, null=True)),
                ('message', models.TextField(blank=True, null=True)),
                ('to', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'From Sayches',
            },
        ),
        migrations.CreateModel(
            name='BlacklistUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('on_post', models.BooleanField(default=False)),
                ('on_login', models.BooleanField(default=False)),
                ('on_message', models.BooleanField(default=False)),
                ('suspended_message', models.TextField(blank=True, default='Sayches suspends accounts which violate the Sayches Rules', null=True)),
                ('user', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Suspended Users',
            },
        ),
        migrations.CreateModel(
            name='Bell',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('targeted_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ring_from', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ring_user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-created_at',),
            },
        ),
        migrations.CreateModel(
            name='Activity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('verb', models.CharField(max_length=255)),
                ('target_id', models.CharField(blank=True, max_length=20, null=True)),
                ('activity_type', models.CharField(choices=[('bell', 'Bell'), ('default', 'default'), ('ping', 'Ping')], default='default', max_length=10)),
                ('read', models.BooleanField(default=False)),
                ('count', models.PositiveIntegerField(default=1)),
                ('receiver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='received_nfs', to=settings.AUTH_USER_MODEL)),
                ('sender', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sended_nfs', to=settings.AUTH_USER_MODEL)),
                ('target_ct', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='target_obj', to='contenttypes.contenttype')),
            ],
            options={
                'verbose_name_plural': 'Activities',
                'ordering': ('-created_at',),
            },
        ),
    ]