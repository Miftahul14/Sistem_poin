from django.contrib import admin
from .models import *
from gurubk.models import *
from walikelas.models import *

class Daftar_Siswa_Admin(admin.ModelAdmin):
    list_display = "nisn", "nama_siswa", "kelas", "wali_kelas"
    
class Daftar_Kelas_Admin(admin.ModelAdmin):
    list_display = "kelas", "nama_kelas", "wali_kelas"
    
class Daftar_Wali_Admin(admin.ModelAdmin):
    list_display = "nip", "nama_wali", "user"
    
class Daftar_Pelanggaran_Admin(admin.ModelAdmin):
    list_display = "nama_pelanggaran", "poin_pelanggaran"
    
class Daftar_Prestasi_Admin(admin.ModelAdmin):
    list_display = "nama_prestasi", "poin_prestasi"
    
    
admin.site.register(Daftar_Siswa, Daftar_Siswa_Admin)
admin.site.register(Daftar_Kelas, Daftar_Kelas_Admin)
admin.site.register(Daftar_Wali, Daftar_Wali_Admin)
admin.site.register(Daftar_Pelanggaran, Daftar_Pelanggaran_Admin)
admin.site.register(Daftar_Prestasi, Daftar_Prestasi_Admin)


