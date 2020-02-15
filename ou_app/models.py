import os

from django.db import models

# Create your models here.
from django.conf import settings
from django.db.models import ForeignKey




class DescriptorCategory(models.Model):
    category = models.CharField(max_length=30)

    def __str__(self):
        return self.category


class DataNodeDescriptor(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    name = models.CharField(max_length=20)
    category = models.ForeignKey(DescriptorCategory,
                                 on_delete=models.SET_NULL,
                                 null=True)
    json = models.TextField()
    template = models.FileField(upload_to='template_opml')

    def __str__(self):
        return f'[{self.category}] {self.name}'


class TransformationInstance(models.Model):
    file = models.FileField(upload_to='input_files')
    transformation = ForeignKey(DataNodeDescriptor,
                                on_delete=models.SET_NULL,
                                null=True)

    def __str__(self):
        return os.path.basename(self.file.path)

