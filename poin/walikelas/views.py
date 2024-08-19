from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from website.decorators import ijinkan_pengguna
from django.contrib import messages
from django.db.models import Count
from django.http import JsonResponse
from .models import *
from administrator.models import *
from gurubk.models import Poin_Pelanggaran

@login_required(login_url='HalamanLogin')
@ijinkan_pengguna(yang_diizinkan=['walikelas']) 
def Beranda_Wali(request):
    wali_kelas = Daftar_Wali.objects.filter(user=request.user).first()
    
    if wali_kelas:
        jumlah_siswa = Daftar_Siswa.objects.filter(wali_kelas=wali_kelas).count()
    else :
        jumlah_siswa = 0
        
    jumlah_prestasi = Daftar_Prestasi.objects.count()
    top_prestasi = (
        Poin_Prestasi.objects
        .select_related('prestasi')
        .values('prestasi__nama_prestasi')
        .annotate(total=Count('prestasi'))
        .order_by('-total')[:3]
    )
    context = {
        'judul' : 'Beranda',
        'menu' : 'Beranda',
        'jumlah_siswa' : jumlah_siswa,
        'jumlah_prestasi' : jumlah_prestasi,
        'top_prestasi' : top_prestasi,
    }
    return render(request, 'beranda_wali.html', context)


# daftar siswa
@login_required(login_url='HalamanLogin')
@ijinkan_pengguna(yang_diizinkan=['walikelas']) 
def Daftar_Siswa_Ad(request):
    siswa = Daftar_Siswa.objects.all().order_by('-id')
    context = {
        'judul' : 'Daftar Siswa',
        'menu' : 'datamaster',
        'submenu' : 'menusiswa',
        'siswa' : siswa,        
    }
    return render(request, 'daftar_siswa.html', context)


@login_required(login_url='HalamanLogin')
@ijinkan_pengguna(yang_diizinkan=['walikelas']) 
def daftar_siswa_wali_kelas(request):
    wali_kelas = get_object_or_404(Daftar_Wali, user=request.user)
    kelas_wali = Daftar_Kelas.objects.filter(wali_kelas=wali_kelas)
    daftar_siswa = Daftar_Siswa.objects.filter(kelas__in = kelas_wali)
    context = {
        'judul' : 'Daftar Siswa',
        'menu' : 'gege',
        'submenu' : 'daftarah',
        'daftar_siswa' :daftar_siswa,
    }
    return render(request, 'daftar_siswa_wali.html', context)
# /daftar siswa


# load nama siswa
def load_nama_kelas(request):
    kelas_id = request.GET.get('kelas_id')
    nama_kelas = Daftar_Kelas.objects.filter(kelas=kelas_id).values('id', 'nama_kelas')
    return JsonResponse(list(nama_kelas), safe=False)

def load_nama_siswa(request):
    nama_kelas_id = request.GET.get('nama_kelas_id')
    siswa = Daftar_Siswa.objects.filter(kelas_id=nama_kelas_id).values('nisn', 'nama_siswa')
    return JsonResponse(list(siswa), safe=False)
# /load nama siswa

# daftar prestasi
@login_required(login_url='HalamanLogin')
@ijinkan_pengguna(yang_diizinkan=['walikelas']) 
def daftar_prestasi_ad(request):
    pres = Daftar_Prestasi.objects.all().order_by('-id')
    context = {
        'judul' : 'Daftar Prestasi',
        'submenu': 'daftarprestasik',
        'menu' : 'DaftarPrestasi',
        'pres' : pres,
    }
    return render(request, 'daftar_prestasi.html', context)


@login_required(login_url='HalamanLogin')
@ijinkan_pengguna(yang_diizinkan=['walikelas']) 
def daftar_prestasi_wali(request):
    pres = Daftar_Prestasi.objects.all().order_by('-id')
    context = {
        'judul' : 'Daftar Prestasi',
        'submenu': 'daftarprestasi',
        'menu' : 'inputPRES',
        'pres' : pres,
    }
    return render(request, 'daftar_prestasi_wali.html', context)
# /daftar prestasi


# poin prestasi
@login_required(login_url='HalamanLogin')
@ijinkan_pengguna(yang_diizinkan=['walikelas']) 
def poin_prestasi_ad(request):
    mprestasi = Poin_Prestasi.objects.all().order_by('-id')
    context = {
        'judul' : 'Poin Prestasi',
        'submenu': 'poinprestasi',
        'menu' : 'DaftarPrestasi',
        'mprestasi' : mprestasi,
    }
    return render(request, 'poin_prestasi.html', context)

@login_required(login_url='HalamanLogin')
@ijinkan_pengguna(yang_diizinkan=['walikelas']) 
def poin_prestasi(request):
    if request.user.groups.filter(name='admin').exists():
        mprestasi = Poin_Prestasi.objects.filter(wali_kelas=wali_kelas).order_by('-id')
    else :
        wali_kelas =get_object_or_404(Daftar_Wali, user=request.user)
        mprestasi = Poin_Prestasi.objects.filter(wali_kelas=wali_kelas).order_by('-id')
    prestasi = Daftar_Prestasi.objects.all()
    context = {
        'judul' : 'Poin Prestasi',
        'submenu': 'poinprestasi',
        'menu' : 'DaftarPrestasi',
        'mprestasi' : mprestasi,
        'prestasi' : prestasi,
    }
    return render(request, 'poin_prestasi_wali.html', context)


@login_required(login_url='HalamanLogin')
@ijinkan_pengguna(yang_diizinkan=['walikelas']) 
def tambah_poin_prestasi(request):
    if request.method == 'POST':
        nisn_siswa = request.POST.get('siswa')
        nama_prestasi = request.POST.get('prestasi')
        catatan = request.POST.get('catatan')
        
        daftar_prestasi = get_object_or_404(Daftar_Prestasi, nama_prestasi=nama_prestasi)
        siswa = get_object_or_404(Daftar_Siswa, nisn=nisn_siswa)
        wali_kelas = get_object_or_404(Daftar_Wali, user=request.user)
        
        Poin_Prestasi.objects.create(
            siswa = siswa,
            wali_kelas = wali_kelas,
            prestasi = daftar_prestasi,
            catatan_prestasi = catatan,           
        )
        messages.success(request, f'Poin prestasi untuk {nisn_siswa} berhasil ditambahkan.')
        return redirect('poin_prestasi')
    
    wali_kelas = get_object_or_404(Daftar_Wali, user=request.user)
    kelas_wali = Daftar_Kelas.objects.filter(wali_kelas=wali_kelas)
    siswa_list = Daftar_Siswa.objects.filter(kelas__in=kelas_wali)
    prestasi = Daftar_Prestasi.objects.all()
    
    prestasi = Daftar_Prestasi.objects.all()
    context = {
        'judul' : 'poin prestasi',
        'prestasi' : prestasi,
        'siswa_list' : siswa_list,
        
    }
    return render(request, 'tambah_poin_wali.html', context)

def edit_poin_prestasi(request, id):
    dapres = get_object_or_404(Poin_Prestasi, id=id)

    if request.method == 'POST':
        prestasi = request.POST.get('prestasi')
        catatan = request.POST.get('catatan')

        item_prestasi = get_object_or_404(Daftar_Prestasi, id=prestasi)

        dapres.prestasi = item_prestasi
        dapres.catatan_prestasi = catatan

        dapres.save()
        messages.success(request, 'Berhasil diperbarui.')
        return redirect('poin_prestasi')
    
    

def hapus_poin_prestasi(request,id):
    pres = get_object_or_404(Poin_Prestasi, id=id)
    pres.delete()
    messages.success(request, 'Poin Prestasi berhasil dihapus.')
    return redirect('poin_prestasi')
# /poin prestasi

