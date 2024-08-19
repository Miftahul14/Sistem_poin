from django.db import models
from django.urls import reverse
from administrator.models import Daftar_Siswa, Daftar_Wali, Daftar_Prestasi

class Poin_Prestasi(models.Model):
    siswa = models.ForeignKey(Daftar_Siswa, on_delete=models.CASCADE, null=True, blank=True)
    wali_kelas = models.ForeignKey(Daftar_Wali, on_delete=models.CASCADE, null=True, blank=True)
    prestasi = models.ForeignKey(Daftar_Prestasi, on_delete=models.CASCADE, null=True, blank=True, related_name="prestasi_wali")
    catatan_prestasi =models.TextField()
    waktu_prestasi = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.siswa.nisn} {self.prestasi}"
    
    class Meta:
        verbose_name_plural = 'Poin Prestasi'
