from django.db import models
from administrator.models import Daftar_Siswa, Daftar_Pelanggaran

class Poin_Pelanggaran(models.Model):
    siswa = models.ForeignKey(Daftar_Siswa, on_delete=models.CASCADE, null=True, blank=True)
    kategori_kelas = models.CharField(max_length=10, null=True, blank=True)
    nama_kelas = models.CharField(max_length=10, null=True, blank=True)
    pelanggaran = models.ForeignKey(Daftar_Pelanggaran, on_delete=models.CASCADE, null=True, blank=True, related_name='pelanggaran_bk')
    catatan_pelanggaran = models.TextField()
    waktu = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.siswa.nisn} {self.pelanggaran}"
    
    class Meta:
        verbose_name_plural = 'Poin Pelanggaran'
        

