from django.urls import path
from .import views

urlpatterns = [
    path('',views.Beranda_Wali, name='Beranda_Wali'),
    
    path('daftar_siswa_wali_kelas/',views.daftar_siswa_wali_kelas, name='daftar_siswa_wali_kelas'),
    
    # path('daftar_siswa_wali/',views.daftar_siswa_wali, name='daftar_siswa_wali'),
    path('ajax/load-nama-kelas/', views.load_nama_kelas, name='ajax_load_nama_kelas'),
    path('ajax/load-nama-siswa/', views.load_nama_siswa, name='ajax_load_nama_siswa'),

    path('daftar_prestasi_wali/',views.daftar_prestasi_wali, name='daftar_prestasi_wali'),
    
    path('poin-prestasi/',views.poin_prestasi, name='poin_prestasi'),
    path('tambah-poin-prestasi/',views.tambah_poin_prestasi, name='tambah_poin_prestasi'),
    path('edit-poin-prestasi/<int:id>/',views.edit_poin_prestasi, name='edit_poin_prestasi'),
    path('hapus-poin-prestasi/<int:id>/', views.hapus_poin_prestasi, name="hapus_poin_prestasi"),
]
