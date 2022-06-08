from django.conf import settings
from django.db import models
from django.utils import timezone

class Vacancies(models.Model):
    company = models.CharField(max_length=100)
    job_title = models.CharField(max_length=100)
    salary = models.PositiveIntegerField()
    skills = models.TextField()
    location = models.TextField()

    def publish(self):
        self.save()

    def __str__(self):
        return self.job_title
