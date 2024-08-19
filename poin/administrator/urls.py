from django.urls import path, include
from .import views

urlpatterns = [
    path('',views.Beranda_Admin, name='Beranda_Admin'),
    path('select2/', include('django_select2.urls')),
    
    # siswa
    path('Daftar_Siswa_Ad/',views.Daftar_Siswa_Ad, name='Daftar_Siswa_Ad'),
    path('tambah_siswa/',views.tambah_siswa, name='tambah_siswa'),
    path('edit_siswa/<int:id>/', views.edit_siswa, name='edit_siswa'),
    path('hapus_siswa/<int:id>/', views.hapus_siswa, name="hapus_siswa"),
    path('administrator/detail_siswa_ad/<int:id>/', views.detail_siswa_ad, name='detail_siswa_ad'),
    path('printpoin/<int:siswa_id>/', views.printpoin, name="printpoin"),
    path('laporan/',views.laporan_view, name='laporan'),
    path('print_pelanggaran/<int:id>/', views.print_pelanggaran, name="print_pelanggaran"),
    path('ajax/load-nama-kelas/', views.load_nama_kelas, name='ajax_load_nama_kelas'),
    path('ajax/load-nama-siswa/', views.load_nama_siswa, name='ajax_load_nama_siswa'),
    # /siswa
    
    # kelas
    path('Kelas_Siswa_Ad/', views.Kelas_Siswa_Ad, name='Kelas_Siswa_Ad'),
    path('kelas/<int:kelas_id>/', views.detail_siswa_kelas, name='detail_siswa_kelas'),
    path('tambah_kelas/', views.tambah_kelas, name='tambah_kelas'),
    path('administrator/takel/',views.takel, name='takel'),
    path('edit_kelas/<int:id>/',views.edit_kelas, name='edit_kelas'),
    path('hapus_kelas/<int:id>/',views.hapus_kelas, name='hapus_kelas'),
    path('promote-class/', views.promote_class, name='promote_class'),
    # /kelas
    
    # wali kelas
    path('Daftar_Wali_Ad/', views.Daftar_Wali_Ad, name='Daftar_Wali_Ad'),
    path('tambah_wali/', views.tambah_wali, name='tambah_wali'),
    path('edit_wali/<int:id>/',views.edit_wali, name='edit_wali'),
    path('hapus_wali/<int:id>/', views.hapus_wali, name="hapus_wali"),
    # /wali kelas
    
    # pelanggaran
    path('daftar_pelanggaran_ad/',views.daftar_pelanggaran_ad, name='daftar_pelanggaran_ad'), 
    path('poin_pelanggaran_ad/',views.poin_pelanggaran_ad, name='poin_pelanggaran_ad'), 
    path('tambah_dapel/', views.tambah_dapel, name="tambah_dapel"),
    path('hapus_dapel/<int:id>/', views.hapus_dapel, name="hapus_dapel"),
    path('edit_pelanggaran/<int:id>/',views.edit_pelanggaran, name='edit_pelanggaran'),
    # /pelanggaran
    
    # prestasi
    path('daftar_prestasi_ad/',views.daftar_prestasi_ad, name='daftar_prestasi_ad'), 
    path('poin_prestasi_ad/',views.poin_prestasi_ad, name='poin_prestasi_ad'), 
    path('tambah_daftar_pre/',views.tambah_daftar_pre, name='tambah_daftar_pre'), 
    path('edit_prestasi/<int:id>/',views.edit_prestasi, name='edit_prestasi'),
    path('hapus_prestasi/<int:id>/', views.hapus_prestasi, name="hapus_prestasi"),
    # /prestasi
]
