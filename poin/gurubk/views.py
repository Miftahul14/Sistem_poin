from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from website.decorators import ijinkan_pengguna
from .models import *
from administrator.models import *
from django.http import JsonResponse
from django.contrib import messages
from django.db.models import Count

@login_required(login_url='HalamanLogin')
@ijinkan_pengguna(yang_diizinkan=['gurubk']) 
def Beranda_Bk(request):
    jumlah_siswa = Daftar_Siswa.objects.count()
    jumlah_pelanggaran = Daftar_Pelanggaran.objects.count()
    top_pelanggaran = (
        Poin_Pelanggaran.objects
        .select_related('pelanggaran')
        .values('pelanggaran__nama_pelanggaran')
        .annotate(total=Count('pelanggaran'))
        .order_by('-total')[:3]
    )
    context = {
        'judul' : 'Beranda',
        'menu' : 'Beranda',
        'jumlah_siswa' : jumlah_siswa,
        'jumlah_pelanggaran' : jumlah_pelanggaran,
        'top_pelanggaran' : top_pelanggaran,
    }
    return render(request, 'beranda_Bk.html', context)


# daftar siswa
@login_required(login_url='HalamanLogin')
@ijinkan_pengguna(yang_diizinkan=['gurubk']) 
def Daftar_Siswa_Ad(request):
    siswa = Daftar_Siswa.objects.all()
    context = {
        'judul' : 'Daftar Siswa',
        'menu' : 'datamaster',
        'submenu' : 'menusiswa',       
        'siswa' : siswa,       
    }
    return render(request, 'daftar_siswa.html', context)

@login_required(login_url='HalamanLogin')
@ijinkan_pengguna(yang_diizinkan=['gurubk']) 
def daftar_siswa_bk(request):
    siswa = Daftar_Siswa.objects.all().order_by('-id')
    context = {
        'judul' : 'Daftar Siswa',
        'menu' : 'siswa',
        'siswa' : siswa,
    }
    return render(request, 'daftar_siswa_bk.html', context)
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
# load nama siswa

# daftar pelanggaran
@login_required(login_url='HalamanLogin')
@ijinkan_pengguna(yang_diizinkan=['gurubk']) 
def daftar_pelanggaran_ad(request):
    dapel = Daftar_Pelanggaran.objects.all().order_by('-id')
    context = {
        'menu': 'pelanggaransiswa',
        'submenu': 'daftarpelanggaran',
        'judul' : 'Daftar Pelanggaran',
        'dapel' : dapel,
        }
    return render(request, 'daftar_pelanggaran.html', context)

@login_required(login_url='HalamanLogin')
@ijinkan_pengguna(yang_diizinkan=['gurubk']) 
def daftar_pelanggaran_bk(request):
    dapel = Daftar_Pelanggaran.objects.all().order_by('-id')
    context = {
        'judul' : 'Input Pelanggaran',
        'menu' : 'inputPEL',
        'dapel' : dapel,
    }
    return render(request, 'daftar_pelanggaran_bk.html', context)
# /daftar pelanggaran


# poin pelanggaran
@login_required(login_url='HalamanLogin')
@ijinkan_pengguna(yang_diizinkan=['gurubk']) 
def poin_pelanggaran_ad(request):
    mpelanggaran = Poin_Pelanggaran.objects.all().order_by('-id')
    context = {
        'menu': 'pelanggaransiswa', 
        'submenu': 'poinpelanggaran',
        'judul' : 'Poin Pelanggaran',
        'mpelanggaran' : mpelanggaran,
        }
    return render(request, 'poin_pelanggaran.html', context)


@login_required(login_url='HalamanLogin')
@ijinkan_pengguna(yang_diizinkan=['gurubk']) 
def poin_pelanggaran(request):
    mpelanggaran = Poin_Pelanggaran.objects.select_related('siswa').all().order_by('-id')
    pelanggaran = Daftar_Pelanggaran.objects.all()
    context = {
        'judul' : 'Input Poin',
        'menu' : 'inputpoin',
        'mpelanggaran' : mpelanggaran,
        'pelanggaran' : pelanggaran,
    }
    return render(request, 'poin_pelanggaran_bk.html', context)


@login_required(login_url='HalamanLogin')
@ijinkan_pengguna(yang_diizinkan=['gurubk']) 
def tambah_poin_pelanggaran(request):
    if request.method == 'POST':
        kategori_kelas = request.POST.get('kategori_kelas')
        nama_kelas_id = request.POST.get('nama_kelas')
        nama_kelas = Daftar_Kelas.objects.get(id=nama_kelas_id)
        nisn_siswa = request.POST.get('siswa')
        pelanggaran_id = request.POST.get('pelanggaran')
        catatan = request.POST.get('catatan')
        
        siswa = get_object_or_404(Daftar_Siswa, nisn=nisn_siswa)
        pelanggaran = get_object_or_404(Daftar_Pelanggaran, id=pelanggaran_id)
        
        Poin_Pelanggaran.objects.create(
            siswa = siswa,
            kategori_kelas = kategori_kelas,
            nama_kelas = nama_kelas.kelas,
            pelanggaran = pelanggaran,
            catatan_pelanggaran = catatan,           
        )
        messages.success(request, f'{nisn_siswa} berhasil ditambahkan.')
        return redirect('poin_pelanggaran')
    
    kategori_kelas = Daftar_Kelas.objects.values_list('kelas', flat=True).distinct()
    pelanggaran = Daftar_Pelanggaran.objects.all()
    context = {
        'judul' : 'poin pelanggaran',
        'kategori_kelas' : kategori_kelas,
        'pelanggaran' : pelanggaran,
        
    }
    return render(request, 'tambah_poin_bk.html', context)

def edit_poin_pelanggaran(request, id):
    dapel = get_object_or_404(Poin_Pelanggaran, id=id)
    
    if request.method == 'POST':
        pelanggaran = request.POST.get('pelanggaran')
        catatan = request.POST.get('catpel')
        
        item_pelanggaran = get_object_or_404(Daftar_Pelanggaran, id=pelanggaran)
        
        dapel.pelanggaran = item_pelanggaran
        dapel.catatan_pelanggaran = catatan
        dapel.save()
        
        messages.success(request, ' berhasil diperbarui.')
        return redirect('poin_pelanggaran')
    
def hapus_poin_pelanggaran(request,id):
    dapel = get_object_or_404(Poin_Pelanggaran, id=id)
    dapel.delete()
    messages.success(request, 'Poin pelanggaran berhasil dihapus.')
    return redirect('poin_pelanggaran')
# /poin pelanggaran



