# Create your models here.
from choices import COLORS_CHOICES, LANGUAGE_CHOICES, SPEC_CHOICES
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


# class CustomUserManager(BaseUserManager):
#     def create_user(self, email, first_name,last_name, , password=None, is_admin=False, is_staff=False,
#                     is_active=True):
#         if not email:
#             raise ValueError("User must have an email")
#         if not password:
#             raise ValueError("User must have a password")
#         if not full_name:
#             raise ValueError("User must have a full name")
#
#         user = self.model(
#             email=self.normalize_email(email)
#         )
#         user.full_name = full_name
#         user.set_password(password)  # change password to hash
#         user.profile_picture = profile_picture
#         user.admin = is_admin
#         user.staff = is_staff
#         user.active = is_active
#         user.save(using=self._db)
#         return user
#
#     def create_superuser(self, email, full_name, profile_picture, password=None, **extra_fields):
#         if not email:
#             raise ValueError("User must have an email")
#         if not password:
#             raise ValueError("User must have a password")
#         if not full_name:
#             raise ValueError("User must have a full name")
#
#         user = self.model(
#             email=self.normalize_email(email)
#         )
#         user.full_name = full_name
#         user.set_password(password)
#         user.profile_picture = profile_picture
#         user.admin = True
#         user.staff = True
#         user.active = True
#         user.save(using=self._db)
#         return user

# TODO https://testdriven.io/blog/django-custom-user-model/
class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(_('first name'), max_length=150, blank=True)
    last_name = models.CharField(_('last name'), max_length=150, blank=True)
    email = models.EmailField(_('email address'), blank=True)
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    age = models.PositiveIntegerField(verbose_name=_('age'), validators=[MaxValueValidator(150)])
    phone = models.BigIntegerField(verbose_name=_('phone'), default=0, blank=True, unique=True)

    # EMAIL_FIELD = 'email'
    # USERNAME_FIELD = 'phone'
    # REQUIRED_FIELDS = ['phone']
    def __str__(self):
        return self.first_name + " " + self.last_name


class Guardian(models.Model):

    banned = models.BooleanField(_('banned'), help_text="Был ли он забанен опекуном через администратора",null=True, blank=True)
    is_send = models.BooleanField(_('is_send'), help_text="отправлять ли отчеты об опекуне",null=True, blank=True)
    relationship = models.CharField(_('relationship'), max_length=150, blank=True, help_text="родство с опекуном",null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(_('first name'), max_length=150, blank=True)
    last_name = models.CharField(_('last name'), max_length=150, blank=True)
    email = models.EmailField(_('email address'), blank=True)
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    phone = models.BigIntegerField(verbose_name=_('phone'), default=0, blank=True, unique=True)
    care_about = models.OneToOneField(Patient, verbose_name=_('care about'), blank=True, null=True, on_delete=models.DO_NOTHING)

    def __str__(self):
        return str(self.first_name) + " " + str(self.last_name)


class PatientSetting(models.Model):
    patient = models.OneToOneField(Patient, verbose_name=_('patient'), on_delete=models.CASCADE)
    color = models.CharField(verbose_name=_("color"), max_length=255, choices=COLORS_CHOICES, default="white")
    font = models.IntegerField(verbose_name=_('font'))
    city = models.CharField(verbose_name=_("city"), max_length=255)
    language = models.CharField(verbose_name=_("language"), max_length=255, choices=LANGUAGE_CHOICES)


class Tokens(models.Model):
    token = models.CharField(verbose_name=_("action"), max_length=255)
    date = models.DateTimeField(verbose_name=_("date"))
    user = models.ForeignKey(Patient, on_delete=models.CASCADE)


class Tariff(models.Model):
    price = models.DecimalField(verbose_name=_("price"), max_digits=20, decimal_places=12)
    date = models.DateTimeField(verbose_name=_("date_start"))
    duration_days = models.PositiveIntegerField(verbose_name=_("duration_days"))
    user = models.ForeignKey(Patient, on_delete=models.CASCADE)


class Tranzaction(models.Model):
    bill = models.CharField(verbose_name=_("bill"), max_length=255)
    date = models.DateTimeField(verbose_name=_("date_start"))
    method = models.CharField(verbose_name=_("billing method"), max_length=255)
    user = models.ForeignKey(Patient, on_delete=models.CASCADE)



class Doctor(models.Model):
    first_name = models.CharField(_('first name'), max_length=150, blank=True)
    last_name = models.CharField(_('last name'), max_length=150, blank=True)
    specialty = models.CharField(_('specialty'), max_length=150, blank=True,choices=SPEC_CHOICES)


class DoctorVisit(models.Model):
    user = models.ManyToManyField(Patient)
    date = models.DateTimeField(verbose_name=_("date_start"))
    doctor = models.ForeignKey(Doctor, on_delete=models.DO_NOTHING)
