# Create your models here.
from choices import DEVISE_CHOICES
from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.
from managment.models import Patient
from medicine.models import Cure


class Report(models.Model):
    patient = models.ForeignKey(Patient, verbose_name=_("user"), on_delete=models.CASCADE)
    title = models.CharField(verbose_name=_("title"), max_length=255)

    class Meta:
        unique_together = [('patient', 'title')]


class ReportDot(models.Model):
    report = models.ForeignKey(Report, verbose_name=_('report'), on_delete=models.CASCADE)
    x = models.FloatField(verbose_name="x")
    y = models.FloatField(verbose_name="y")


class Devise(models.Model):
    api = models.CharField(verbose_name=_("api"), max_length=255)
    type_of_devise = models.CharField(verbose_name=_("type_of_devise"), max_length=255, choices=DEVISE_CHOICES)


class Logs(models.Model):
    action = models.CharField(verbose_name=_("action"), max_length=255)
    date = models.DateTimeField(verbose_name=_("date"))


class MissedMed(models.Model):
    patient = models.ForeignKey(Patient, verbose_name=_("user"), on_delete=models.CASCADE)
    med = models.ForeignKey(Cure, on_delete=models.CASCADE)
    date = models.DateTimeField(verbose_name=_("date"))
    is_informed = models.CharField(verbose_name=_("is_informed"), max_length=255, help_text="is informed guardian")


class TakenMed(models.Model):
    patient = models.ForeignKey(Patient, verbose_name=_("user"), on_delete=models.CASCADE)
    med = models.ForeignKey(Cure, on_delete=models.CASCADE)
    date = models.DateTimeField(verbose_name=_("date"))
    is_late = models.BooleanField(verbose_name=_("is_late"), max_length=255)
    report = models.BooleanField(verbose_name=_("report"), max_length=255, help_text = "был ли включен в отчет")
