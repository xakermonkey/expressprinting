import logging
from django.db import models
from .cups_connection import set_connection_cups
# Create your models here.

logger = logging.getLogger(__name__)


class POS(models.Model):
    name = models.CharField(max_length=255, verbose_name="Наименование точки печати")
    ip = models.CharField(max_length=255, verbose_name="IP принтера")
    name_printer = models.CharField(max_length=500, verbose_name='Название принтера')
    scheme_img = models.ImageField(upload_to='pos', blank=True, null=True, verbose_name="Схема")
    slug = models.CharField(max_length=255, verbose_name="Ссылка", blank=True, null=True, unique=True)

    def save(self, *args, **kwargs):
        con = set_connection_cups()
        con.addPrinter(name=self.name_printer)
        con.setPrinterDevice(self.name_printer, f"ipp://{self.ip}:23684/ipp/print")
        con.acceptJobs(self.name_printer)
        super(POS, self).save(*args, **kwargs)
 
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
    pos = models.ForeignKey(POS, on_delete=models.CASCADE, verbose_name='Точка в которой заказали печать')
    price_per_list = models.DecimalField(decimal_places=2, max_digits=5, verbose_name="Цена за лист")
    list_count = models.IntegerField(verbose_name="Общее количество страниц", null=True, blank=True)
    amount = models.DecimalField(decimal_places=2,max_digits=9, verbose_name="Сумма заказа", null=True, blank=True)
    documents = models.ManyToManyField('Doc', related_name='order')

    def __str__(self):
        return f"Заказ в {self.date_create} в точке {self.pos}"

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

class StaffOrder(models.Model):
    date_print = models.DateField(verbose_name="Дата печати", blank=True, null=True)
    pos = models.ForeignKey(POS, on_delete=models.CASCADE, verbose_name='Точка печати')
    documents = models.ManyToManyField('Doc', related_name='staff_print')

    def __str__(self):
        return f"Печать сотрудников"

    class Meta:
        verbose_name = 'Печать сотрудника'
        verbose_name_plural = 'Печать сотрудника'



class Doc(models.Model):
    file = models.FileField(verbose_name='Файл', upload_to='templates/static/orders', max_length=1000)
    name = models.CharField(max_length=255, verbose_name="Название файла", blank=True, null=True)
    stati_path = models.CharField(max_length=255, verbose_name="Путь до файла", blank=True, null=True)
    copy = models.IntegerField(verbose_name="Количетво копий")

    def __str__(self):
        return f"Файл {self.file.name}"
    class Meta:
        verbose_name = 'Файл'
        verbose_name_plural = 'Файлы'
