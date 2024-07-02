from django.db import models

class Test1(models.Model):
    keywords = models.TextField(db_column='Keywords', blank=True, primary_key=True)
    count = models.BigIntegerField(db_column='Count', blank=True, null=True)

    class Meta:
        managed = False
        db_table = None  # 테이블 이름을 나중에 동적으로 설정

