from django.db import models

# Create your models here.





class POS(models.Model):
    name = models.CharField(max_length=255, verbose_name="Наименование точки печати")
    ip = models.CharField(max_length=255, verbose_name="IP принтера")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Точка печати'
        verbose_name_plural = 'Точки печати'



class Rates(models.Model):
    pos = models.ForeignKey(POS, on_delete=models.CASCADE, verbose_name="Точка печати")
    date = models.DateField()
    price_per_list = models.DecimalField(decimal_places=2,max_digits=5, verbose_name="Цена за лист")


    def __str__(self):
        return f"Тариф для {self.pos}"


    class Meta:
        verbose_name = 'Тариф'
        verbose_name_plural = 'Тарифы'


class Order(models.Model):
    date_create = models.DateField(verbose_name="Дата создания заказа")
    date_print = models.DateField(verbose_name="Дата печати", blank=True, null=True)
    number = models.CharField(max_length=255, verbose_name="Номер заказа")
    code = models.IntegerField(verbose_name="Код")
    pos = models.ForeignKey(POS, on_delete=models.CASCADE, verbose_name='Точка в которой заказали печать')
    price_per_list = models.DecimalField(decimal_places=2,max_digits=5, verbose_name="Цена за лист")
    list_count = models.IntegerField(verbose_name="Общее количество страниц", null=True, blank=True)
    amount = models.DecimalField(decimal_places=2,max_digits=9, verbose_name="Сумма заказа", null=True, blank=True)
    documents = models.ManyToManyField('Doc', related_name='order')

    def __str__(self):
        return f"Заказ в {self.date_create} в точке {self.pos}"

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'



class Doc(models.Model):
    file = models.FileField(verbose_name='Файл', upload_to='templates/static/orders')
    name = models.CharField(max_length=255, verbose_name="Название файла", blank=True, null=True)
    stati_path = models.CharField(max_length=255, verbose_name="Путь до файла", blank=True, null=True)
    copy = models.IntegerField(verbose_name="Количетво копий")

    def __str__(self):
        return f"Файл {self.file.name}"
    class Meta:
        verbose_name = 'Файл'
        verbose_name_plural = 'Файлы'





