from django.db import models
from portal.models import Service


class FAQ(models.Model):
    question = models.CharField(max_length=1000, blank=False)
    answer = models.CharField(max_length=3000, blank=False)
    service = models.ForeignKey(Service, blank=True, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.question[0:20] + ": " + self.answer[0:20]
