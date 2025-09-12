from django.db import models

# Create your models here.
class carInfo(models.Model):
    id = models.AutoField('id', primary_key = True)
    brand = models.CharField('品牌', max_length=255, default='')
    carName = models.CharField('车名', max_length=255, default='')
    carImg = models.CharField('图片链接', max_length=255, default='')
    saleVolume = models.CharField('销量', max_length=255, default='')
    price = models.CharField('价格', max_length=255, default='')
    manufacturer = models.CharField('厂商', max_length=255, default='')
    rank = models.CharField('排名', max_length=255, default='')
    carModel = models.CharField('车型', max_length=255, default='')
    energyType = models.CharField('能源类型', max_length=255, default='')
    marketTime = models.CharField('上市时间', max_length=255, default='')
    insure = models.CharField('保修时间', max_length=255, default='')
    creteTime = models.DateTimeField('创建时间', auto_now_add=True)
    class Meta:
        db_table = 'carInfo'

# 用户
class User(models.Model):
    id = models.AutoField('id', primary_key=True)
    username = models.CharField('用户名', max_length=8, default='')
    password = models.CharField('密码', max_length=255, default='')
    createTime = models.DateTimeField('创建时间', auto_now_add=True)
    class Meta:
        db_table = 'user'

# 所有车辆信息表
class AllCarInfo(models.Model):
    id = models.AutoField('id', primary_key = True)
    brand = models.CharField('品牌', max_length=255, default='')
    carName = models.CharField('车名', max_length=255, default='')
    carImg = models.CharField('图片链接', max_length=255, default='')
    saleVolume = models.CharField('销量', max_length=255, default='')
    price = models.CharField('价格', max_length=255, default='')
    manufacturer = models.CharField('厂商', max_length=255, default='')
    rank = models.CharField('排名', max_length=255, default='')
    carModel = models.CharField('车型', max_length=255, default='')
    energyType = models.CharField('能源类型', max_length=255, default='')
    marketTime = models.CharField('上市时间', max_length=255, default='')
    insure = models.CharField('保修时间', max_length=255, default='')
    creteTime = models.DateTimeField('创建时间', auto_now_add=True)
    class Meta:
        db_table = 'allcarinfo'

# 用户车辆详情
class UserCarDetail(models.Model):
    id = models.AutoField('id', primary_key=True)
    car_name = models.CharField('车辆名字', max_length=255, default='')
    car_model = models.CharField('车辆型号', max_length=255, default='')
    mileage = models.FloatField('车辆公里数', default=0)
    purchase_date = models.DateField('车辆购买时间')
    configuration = models.TextField('车辆配置', default='')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    car = models.ForeignKey('carInfo', on_delete=models.SET_NULL, null=True, blank=True)
    createTime = models.DateTimeField('创建时间', auto_now_add=True)
    class Meta:
        db_table = 'user_car_detail'