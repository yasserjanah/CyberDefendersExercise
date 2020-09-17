from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Instance(models.Model):
    user     = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Owner")
    task_id  = models.CharField(verbose_name="Task ID", max_length=100, blank=False)
    name     = models.CharField(verbose_name="Name", max_length=30, blank=False)
    image    = models.CharField(verbose_name="Image", max_length=50, blank=False)
    date     = models.DateTimeField(verbose_name="Created at", auto_now_add=True)
    status   = models.CharField(verbose_name="Status", max_length=30, blank=False)

    def __str__(self):
        return self.name
