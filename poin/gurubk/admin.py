from django.contrib import admin
from .models import *

class Poin_Pelanggaran_Admin(admin.ModelAdmin):
    list_display = "siswa", "kategori_kelas", "nama_kelas", "pelanggaran", "catatan_pelanggaran", "waktu"
    
admin.site.register(Poin_Pelanggaran, Poin_Pelanggaran_Admin)

