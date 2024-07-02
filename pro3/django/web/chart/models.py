from django.db import models

# Create your models here.


# class SalesData(models.Model):
#     date = models.DateField()
#     sales = models.DecimalField(max_digits=10, decimal_places=2)

#     def __str__(self):
#         return f"{self.date}: {self.sales}"
    

class Test(models.Model):
    keywords = models.TextField(db_column='Keywords', blank=True, primary_key=True)  # Field name made lowercase.
    count = models.BigIntegerField(db_column='Count', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'test'
