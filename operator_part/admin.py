from django.contrib import admin
from .models import *
# Register your models here.


admin.site.site_header = 'Администрирование Express Printing'
admin.site.site_title = 'Express Printing'

admin.site.register(POS)
admin.site.register(Rates)
admin.site.register(Order)
admin.site.register(Doc)
