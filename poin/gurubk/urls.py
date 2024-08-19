from django.urls import path
from .import views

urlpatterns = [
    path('',views.Beranda_Bk, name='Beranda_Bk'),
    
    path('daftar_siswa_bk/',views.daftar_siswa_bk, name='daftar_siswa_bk'),
    
    path('daftar_pelanggaran_bk/',views.daftar_pelanggaran_bk, name='daftar_pelanggaran_bk'),

    # poin
    path('poin-pelanggaran/', views.poin_pelanggaran, name='poin_pelanggaran'),
    path('tambah-poin-pelanggaran/', views.tambah_poin_pelanggaran, name='tambah_poin_pelanggaran'),
    path('edit-poin-pelanggaran/<int:id>/',views.edit_poin_pelanggaran, name='edit_poin_pelanggaran'),
    path('hapus-poin-pelanggaran/<int:id>/', views.hapus_poin_pelanggaran, name="hapus_poin_pelanggaran"),
    # /poin
    
    # ajax
    path('ajax/load-nama-kelas/', views.load_nama_kelas, name='ajax_load_nama_kelas'),
    path('ajax/load-nama-siswa/', views.load_nama_siswa, name='ajax_load_nama_siswa'),
    # /ajax
]
