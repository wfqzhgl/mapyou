#-*-coding:utf-8-*-

from django.db import models


class DataLotteryShsq(models.Model):
    code = models.CharField("code", max_length=32, unique=True)
    reds = models.CharField("reds", max_length=32)
    blue = models.CharField("blue", max_length=32)
    award_total = models.PositiveIntegerField("award_total")

    count_1 = models.PositiveIntegerField("count_1")
    award_1 = models.PositiveIntegerField("award_1")
    count_2 = models.PositiveIntegerField("count_2")
    award_2 = models.PositiveIntegerField("award_2")
    bet_total = models.PositiveIntegerField("bet_total")
    date = models.DateField("date", unique=True)

    created = models.DateTimeField("创建时间", auto_now_add=True)

    class Meta:
        verbose_name = "历史数据"
        verbose_name_plural = "历史数据管理"
        ordering = ['-date']

    def __unicode__(self):
        return self.code + ":" + str(self.date)

