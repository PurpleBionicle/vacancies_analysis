from django.conf import settings
from django.db import models
from django.utils import timezone


class Vacancies(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    salary = models.CharField(max_length=100)
    skills_name = models.CharField(max_length=1000)
