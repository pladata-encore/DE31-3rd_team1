from django.db import models

# Create your models here.


class Test(models.Model):
    keywords = models.TextField(db_column='Keywords', blank=True, primary_key=True)  # Field name made lowercase.
    count = models.BigIntegerField(db_column='Count', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'test'
