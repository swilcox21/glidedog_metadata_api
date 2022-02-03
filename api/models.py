from tkinter import CASCADE
from django.db import models
from django.utils.translation import gettext_lazy as _

class Dataset(models.Model):
    name = models.CharField(max_length=50)
    owner = models.CharField(max_length=50)
    version = models.IntegerField(default=1)
    current = models.BooleanField(default=True)
    def __int__(self):
        return self.name
    def delete(self):
        self.current = False
        super(Dataset, self).save()

class Table(models.Model):
    name = models.CharField(max_length=50)
    rows = models.IntegerField()
    version = models.IntegerField(default=1)
    current = models.BooleanField(default=True)
    dataset = models.ManyToManyField(Dataset, related_name='table')
    def __str__(self):
        return self.name
    def delete(self):
        dataset = Dataset.objects.filter(table__id=self.id).last()
        tables_d = Table.objects.filter(dataset__id=dataset.id)
        dataset.pk = None
        dataset.version = dataset.version + 1
        dataset.save()
        for t in tables_d:
            t.dataset.add(dataset)
        self.dataset.remove(dataset)
        self.current = False
        super(Table, self).save()

class Column(models.Model):
    name = models.CharField(max_length=50)
    type = models.CharField(max_length=50)
    rows = models.IntegerField()
    table = models.ForeignKey(Table, on_delete=models.CASCADE, related_name='column')
    def __str__(self):
        return self.name
