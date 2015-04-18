# -*-coding:utf-8-*-

from django.db import models
from django.core.urlresolvers import reverse

class Patient(models.Model):
    """
    姓名　性别　年龄　住址　电话
    现病史　既往史　中医诊断　西医诊断
    西医检资料（照片）　结论：　　处方用药：
    初诊时间　复诊时间
    """
    GENDER_CHOICES = (
        (0, u'男'),
        (1, u'女'),
    )
    name = models.CharField("name", max_length=50)
    gender = models.SmallIntegerField("性别", choices=GENDER_CHOICES, default=0)
    age = models.PositiveIntegerField("age", default=0)
    ID_num = models.CharField("身份证", max_length=20, blank=True, null=True)
    address = models.CharField("address", max_length=200, blank=True, null=True)
    phone = models.CharField("电话", max_length=50, blank=True, null=True)
    created = models.DateTimeField("创建时间", auto_now_add=True)
#     cell = models.CharField("手机", max_length=50)
    def __unicode__(self):
        return self.name
    class Meta:
#        unique_together = (("sid", "desc"),)
        verbose_name = '患者'
        verbose_name_plural = '患者管理'


class BCategory(models.Model):
    """
    疾病分类
    """
    name = models.CharField("name", max_length=50, unique=True)
    desc = models.CharField("描述", max_length=200, blank=True, null=True)
    created = models.DateTimeField("创建时间", auto_now_add=True)
    def __unicode__(self):
        return self.name
    class Meta:
#        unique_together = (("sid", "desc"),)
        verbose_name = '分类名称'
        verbose_name_plural = '分类管理'
        
class BType(models.Model):
    """
    疾病名称
    """
    name = models.CharField("name", max_length=50, unique=True)
    category = models.ForeignKey("BCategory", verbose_name="所属分类", blank=True, null=True)
    desc = models.CharField("描述", max_length=200, blank=True, null=True)
    created = models.DateTimeField("创建时间", auto_now_add=True)
    def __unicode__(self):
        return self.name
    class Meta:
#        unique_together = (("sid", "desc"),)
        verbose_name = '疾病名称'
        verbose_name_plural = '疾病名称管理'

class BHistory(models.Model):
    """
    姓名　性别　年龄　住址　电话
    现病史　既往史　中医诊断　西医诊断
    西医检资料（照片）　结论：　　处方用药：
    初诊时间　复诊时间
    """
    date = models.DateField('日期')
    patient = models.ForeignKey("Patient", verbose_name="所属病人")
    btype = models.ForeignKey("BType", verbose_name="所属病")
    his_desc = models.TextField("既往史", max_length=100, blank=True, null=True)
    zhy_desc = models.TextField("中医诊断", max_length=100, blank=True, null=True)
    xy_desc = models.TextField("西医诊断", max_length=100, blank=True, null=True)
    xy_img = models.FileField("西医检资料", upload_to='media_file', help_text='', blank=True, null=True)
    diagnosis = models.TextField("结论", max_length=200, blank=True, null=True)
    prescription = models.TextField("处方用药", max_length=300, blank=True, null=True)
    other_desc = models.CharField("备注", max_length=200, blank=True, null=True)
    created = models.DateTimeField("创建时间", auto_now_add=True)
#     cell = models.CharField("手机", max_length=50)
    def __unicode__(self):
        return self.date.strftime('%Y-%m-%d') + '-' + self.patient.name
    class Meta:
#        unique_together = (("sid", "desc"),)
        verbose_name = '就诊经历'
        verbose_name_plural = '就诊经历管理'
        
