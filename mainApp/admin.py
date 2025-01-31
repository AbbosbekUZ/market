from django.contrib import admin
from .models import Bolim, Mahsulot, Kirim, Xarajat, Sotuv

@admin.register(Bolim)
class BolimAdmin(admin.ModelAdmin):
    list_display = ('nom',)
    search_fields = ('nom',)

@admin.register(Mahsulot)
class MahsulotAdmin(admin.ModelAdmin):
    list_display = ('nom', 'narx1', 'narx2', 'miqdor', 'olchov', 'brend', 'bolim')
    list_filter = ('bolim', 'olchov', 'brend')
    search_fields = ('nom', 'brend')

@admin.register(Kirim)
class KirimAdmin(admin.ModelAdmin):
    list_display = ('sana', 'mahsulot__nom', 'miqdor', 'narx')
    list_filter = ('sana', 'mahsulot__nom')
    search_fields = ('mahsulot__nom',)

@admin.register(Xarajat)
class XarajatAdmin(admin.ModelAdmin):
    list_display = ('sana', 'miqdor', 'izoh')
    search_fields = ('izoh',)

@admin.register(Sotuv)
class SotuvAdmin(admin.ModelAdmin):
    list_display = ('sana', 'mahsulot', 'miqdor', 'jami_summa', 'izoh')
    list_filter = ('sana', 'mahsulot')
    search_fields = ('mahsulot__nom',)
