# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


class AccountsCustomuserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)


class AccountsCustomuser(AbstractBaseUser, PermissionsMixin):
    id = models.BigAutoField(primary_key=True)
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()
    email = models.CharField(unique=True, max_length=254)
    company_name = models.CharField(max_length=30)
    number_of_employer = models.CharField(max_length=30)
    has_permission = models.BooleanField()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []  # Add fields that are required to create a user

    objects = AccountsCustomuserManager()

    class Meta:
        managed = False
        db_table = 'accounts_customuser'



class AccountsCustomuserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    customuser = models.ForeignKey(AccountsCustomuser, models.DO_NOTHING)
    group = models.ForeignKey('AuthGroup', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'accounts_customuser_groups'
        unique_together = (('customuser', 'group'),)


class AccountsCustomuserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    customuser = models.ForeignKey(AccountsCustomuser, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'accounts_customuser_user_permissions'
        unique_together = (('customuser', 'permission'),)


class AccountsOrder(models.Model):
    id = models.BigAutoField(primary_key=True)
    date_created = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=255, blank=True, null=True)
    customer = models.ForeignKey(AccountsCustomuser, models.DO_NOTHING, blank=True, null=True)
    product = models.ForeignKey('Students', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'accounts_order'


class AppUser(models.Model):
    id = models.BigAutoField(primary_key=True)
    username = models.CharField(unique=True, max_length=150)
    email = models.CharField(unique=True, max_length=254)
    password = models.CharField(max_length=128)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    date_joined = models.DateTimeField()
    is_active = models.BooleanField()
    bpp = models.BooleanField()
    cm = models.BooleanField()
    dynamics = models.BooleanField()
    ed = models.BooleanField()
    scrutineering = models.BooleanField()
    statics = models.BooleanField()

    class Meta:
        # managed = False
        db_table = 'appuser'
        verbose_name = 'AppUser'
        verbose_name_plural = 'AppUsers'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class Competition(models.Model):
    name = models.CharField(max_length=255)
    country = models.CharField(max_length=255, blank=True, null=True)
    year = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'competition'
        verbose_name = 'Competition'
        verbose_name_plural = 'Competitions'


class CompetitionTeams(models.Model):
    name = models.CharField(max_length=255)
    car_number = models.CharField(max_length=255, blank=True, null=True)
    university = models.CharField(max_length=255, blank=True, null=True)
    competition = models.ForeignKey(Competition, models.DO_NOTHING, blank=True, null=True, related_name='competition_teams')
    recognition_id = models.CharField(unique=True)
    country = models.CharField(max_length=255, blank=True, null=True)
    team = models.ForeignKey('Teams', models.DO_NOTHING, blank=True, null=True, related_name='competition_entries')

    class Meta:
        managed = False
        db_table = 'competition_teams'
        verbose_name = 'Competition Team'
        verbose_name_plural = 'Competition Teams'


class CompetitionTeamstudents(models.Model):
    student = models.ForeignKey('Students', models.DO_NOTHING, blank=True, null=True)
    team = models.ForeignKey(CompetitionTeams, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'competition_teamstudents'
        verbose_name = 'CompetitionTeam Student'
        verbose_name_plural = 'CompetitionTeam Students'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AccountsCustomuser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class QuestionsQuestions(models.Model):
    question = models.TextField(blank=True, null=True)
    answer = models.TextField(blank=True, null=True)
    is_active = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'questions_questions'


class Students(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    university = models.CharField(max_length=255, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    email = models.CharField(max_length=255, blank=True, null=True)
    mobile_phone_number = models.CharField(max_length=255, blank=True, null=True)
    category = models.CharField(max_length=255, blank=True, null=True)
    position = models.CharField(max_length=255, blank=True, null=True)
    level = models.CharField(max_length=255, blank=True, null=True)
    estimate_year_of_graduation = models.IntegerField(blank=True, null=True)
    specialisation = models.CharField(max_length=255, blank=True, null=True)
    experience = models.IntegerField(blank=True, null=True)
    price = models.IntegerField(blank=True, null=True)
    study = models.CharField(max_length=255, blank=True, null=True)
    country = models.CharField(max_length=255, blank=True, null=True)
    driver = models.CharField(max_length=255, blank=True, null=True)
    eso = models.CharField(max_length=255, blank=True, null=True)
    role_at_competition = models.CharField(max_length=255, blank=True, null=True)
    role_bonus = models.IntegerField(blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)
    gender = models.CharField(max_length=255, blank=True, null=True)
    blood_type = models.CharField(max_length=255, blank=True, null=True)
    emergency_contact_email = models.CharField(max_length=255, blank=True, null=True)
    emergency_contact_full_name = models.CharField(max_length=255, blank=True, null=True)
    emergency_contact_phone = models.CharField(max_length=255, blank=True, null=True)
    health_insurance_card = models.CharField(max_length=255, blank=True, null=True)
    relation_to_emergency_contact = models.CharField(max_length=255, blank=True, null=True)
    mobile_phone_number_test = models.CharField(max_length=128, blank=True, null=True)
    toggle = models.BooleanField(blank=True, null=True)
    bullet_points = models.TextField()  # This field type is a guess.
    experience_description = models.TextField()  # This field type is a guess.
    long_description = models.TextField(blank=True, null=True)
    short_description = models.TextField(blank=True, null=True)
    active = models.BooleanField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'students'
        verbose_name = 'Student'
        verbose_name_plural = 'Students'


class Teams(models.Model):
    fsg = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    university = models.CharField(max_length=255, blank=True, null=True)
    country = models.CharField(max_length=255, blank=True, null=True)
    category = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    fsg_link = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'teams'
        verbose_name = 'Team'
        verbose_name_plural = 'Teams'


class StaticQuestion(models.Model):
    id = models.AutoField(primary_key=True)
    field_name = models.CharField(max_length=255)
    max_score = models.IntegerField(blank=True, null=True)
    category = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'static_question'
        verbose_name = 'StaticQuestion'
        verbose_name_plural = 'StaticQuestions'


class StaticAnswer(models.Model):
    id = models.AutoField(primary_key=True)
    team = models.ForeignKey(CompetitionTeams, models.DO_NOTHING, db_column='team_id', blank=True, null=True,)
    user = models.ForeignKey(AppUser, models.DO_NOTHING, db_column='user_id', blank=True, null=True)
    score = models.IntegerField(blank=True, null=True)
    question = models.ForeignKey(StaticQuestion, models.DO_NOTHING, db_column='question_id', blank=True, null=True)

    class Meta:
        db_table = 'static_answer'
        verbose_name = 'StaticAnswer'
        verbose_name_plural = 'StaticAnswers'


class StaticReport(models.Model):
    id = models.AutoField(primary_key=True)
    team = models.ForeignKey(CompetitionTeams, models.DO_NOTHING, db_column='team_id', blank=True, null=True,)
    user = models.ForeignKey(AppUser, models.DO_NOTHING, db_column='user_id', blank=True, null=True)
    notes = models.TextField(null=True, blank=True)
    presenter = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'static_report'
        verbose_name = 'StaticReport'
        verbose_name_plural = 'StaticReports'

