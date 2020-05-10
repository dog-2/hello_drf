from django.db import models

# Create your models here.
class Car(models.Model):
    name = models.CharField(max_length=16, unique=True, verbose_name='车名')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='价格')
    brand = models.CharField(max_length=16, verbose_name='品牌')

    class Meta:
        db_table = 'api_car'
        verbose_name = '汽车表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name