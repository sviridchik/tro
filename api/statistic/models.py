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
    patient = models.ForeignKey(Patient, verbose_name=_("user"), on_delete=models.CASCADE)
    report = models.ForeignKey(Report, verbose_name=_('report'), on_delete=models.CASCADE)
    x = models.FloatField(verbose_name="x",help_text="колво принятых")
    y = models.FloatField(verbose_name="y",help_text="колво не принятых")


class Devise(models.Model):
    patient = models.ForeignKey(Patient, verbose_name=_("user"), on_delete=models.CASCADE)
    api = models.CharField(verbose_name=_("api"), max_length=255)
    type_of_devise = models.CharField(verbose_name=_("type_of_devise"), max_length=255, choices=DEVISE_CHOICES)


class Logs(models.Model):
    patient = models.ForeignKey(Patient, verbose_name=_("user"), on_delete=models.CASCADE)
    action = models.CharField(verbose_name=_("action"), max_length=255)
    date = models.DateTimeField(verbose_name=_("date"))


class MissedMed(models.Model):
    patient = models.ForeignKey(Patient, verbose_name=_("user"), on_delete=models.CASCADE)
    med = models.ForeignKey(Cure, on_delete=models.CASCADE)
    date = models.DateTimeField(verbose_name=_("date"))
    is_informed = models.BooleanField(verbose_name=_("is_informed"), help_text="is informed guardian")


class TakenMed(models.Model):
    patient = models.ForeignKey(Patient, verbose_name=_("user"), on_delete=models.CASCADE)
    med = models.ForeignKey(Cure, on_delete=models.CASCADE)
    date = models.DateTimeField(verbose_name=_("date"))
    is_late = models.BooleanField(verbose_name=_("is_late"))
    report = models.BooleanField(verbose_name=_("report"), help_text = "был ли включен в отчет")

class Label(models.Model):
    user = models.ManyToManyField(Patient)
    title = models.CharField(verbose_name=_("title"), max_length=255)


class Achievement(models.Model):
    user = models.ForeignKey(Patient, on_delete=models.CASCADE)
    days_attended = models.PositiveIntegerField(verbose_name=_("days_attended"))
    days_no_miss = models.PositiveIntegerField(verbose_name=_("days_no_miss"))
    number_in_time = models.PositiveIntegerField(verbose_name=_("number_in_time"))

    # Гуишкой похвалу
    praise_from_guard = models.PositiveIntegerField(verbose_name=_("praise_from_guard"),
                                                    help_text="количество раз похвалы")
