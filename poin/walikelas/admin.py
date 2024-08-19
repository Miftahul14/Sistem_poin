from django.contrib import admin
from .models import *

class Poin_Prestasi_Admin(admin.ModelAdmin):
    list_display = "siswa", "wali_kelas", "prestasi", "catatan_prestasi", "waktu_prestasi"
    
admin.site.register(Poin_Prestasi, Poin_Prestasi_Admin)
