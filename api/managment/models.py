# Create your models here.
from choices import COLORS_CHOICES, LANGUAGE_CHOICES
from django.contrib.auth.models import AbstractBaseUser
from django.core.validators import MaxValueValidator
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import UserManager
from django.contrib.auth.models import User


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
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    age = models.PositiveIntegerField(verbose_name=_('age'), validators=[MaxValueValidator(150)])
    phone = models.BigIntegerField(verbose_name=_('phone'), default=0, blank=True, unique=True)
    care_about = models.ManyToManyField('self',verbose_name=_('care about'),blank=True,null=True)

    # EMAIL_FIELD = 'email'
    # USERNAME_FIELD = 'phone'
    # REQUIRED_FIELDS = ['phone']
    def __str__(self):
        return self.first_name+" "+self.last_name

class PatientSetting(models.Model):
    patient = models.OneToOneField(Patient, verbose_name=_('patient'), on_delete=models.CASCADE)
    color = models.CharField(verbose_name=_("color"), max_length=255, choices=COLORS_CHOICES, default="white")
    font = models.IntegerField(verbose_name=_('font'))
    city = models.CharField(verbose_name=_("city"), max_length=255)
    language = models.CharField(verbose_name=_("language"), max_length=255, choices=LANGUAGE_CHOICES)


class Report(models.Model):
    patient = models.ForeignKey(Patient, verbose_name=_("user"), on_delete=models.CASCADE)
    title = models.CharField(verbose_name=_("title"), max_length=255)

    class Meta:
        unique_together = [('patient', 'title')]


class ReportDot(models.Model):
    report = models.ForeignKey(Report, verbose_name=_('report'), on_delete=models.CASCADE)
    x = models.FloatField(verbose_name="x")
    y = models.FloatField(verbose_name="y")
