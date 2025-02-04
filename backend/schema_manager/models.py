from django.db import models


class Schema(models.Model):
    table_name = models.CharField(max_length=100, unique=True)
    fields = models.JSONField()

    def __str__(self):
        return self.table_name
