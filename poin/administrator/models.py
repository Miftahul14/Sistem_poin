from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


class Daftar_Wali(models.Model):
    nip = models.CharField(max_length=20, unique=True)
    nama_wali = models.CharField(max_length=50)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True,blank=True)
    
    def __str__(self):
        return f"{self.nip} - {self.nama_wali}"
    
    class Meta:
        verbose_name_plural = 'Wali Kelas'

class Daftar_Kelas(models.Model):
    kelas = models.CharField(max_length=10)
    nama_kelas = models.CharField(max_length=10)
    wali_kelas = models.ForeignKey(Daftar_Wali, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.kelas} - {self.nama_kelas}"
    
    class Meta:
        verbose_name_plural = 'Daftar Kelas'
        
        
class Daftar_Siswa(models.Model):
    nisn = models.CharField(max_length=20, unique=True)
    nama_siswa = models.CharField(max_length=50)
    kelas = models.ForeignKey(Daftar_Kelas, on_delete=models.CASCADE)
    wali_kelas = models.ForeignKey(Daftar_Wali, on_delete=models.CASCADE, null=True, blank=True)
    
    def __str__(self):
        return f"{self.nisn} - {self.nama_siswa}"
    
    class Meta:
        verbose_name_plural = 'Daftar Siswa'
        
    
class Daftar_Pelanggaran(models.Model):
    nama_pelanggaran = models.CharField(max_length=50)
    poin_pelanggaran = models.IntegerField()
    
    def __str__(self):
        return f"{self.nama_pelanggaran} - {self.poin_pelanggaran}"
    
    class Meta:
        verbose_name_plural = 'Daftar Pelanggaran'
    
    
class Daftar_Prestasi(models.Model):
    nama_prestasi = models.CharField(max_length=50)
    poin_prestasi = models.IntegerField()
    
    def __str__(self) :
        return f"{self.nama_prestasi} - {self.poin_prestasi}"
    
    class Meta:
        verbose_name_plural = 'Daftar Prestasi'
    

