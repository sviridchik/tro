import factory
from django.contrib.auth.models import User
from faker import Faker

from medicine.models import Cure, Schedule

fake = Faker()


class CureFactory(factory.django.DjangoModelFactory):
    title = "Джес Плюс"
    dose = 1
    schedule = None
    type = "ТАБЛЕТКА"


    class Meta:
        model = Cure

class ScheduleFactory(factory.django.DjangoModelFactory):
    cycle_start = models.DateField(verbose_name="start")
    cycle_end = models.DateField(verbose_name="end")
    frequency = models.IntegerField(verbose_name="frequency", validators=[MinValueValidator(0)])
    time = "se"
    strick = True


class Meta:
        model = Cure
