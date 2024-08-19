from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from website.decorators import ijinkan_pengguna, pilihan_login
from .models import *
from gurubk.models import *
from walikelas.models import *
from django.http import JsonResponse
from django.contrib import messages
from django.db.models import Count, Subquery, OuterRef, Sum
from django.db.models.functions import Coalesce
from .forms import *
from django.contrib.auth.models import User,Group
from django.utils.dateparse import parse_date


@login_required(login_url='HalamanLogin')
@pilihan_login
def Beranda_Admin(request):
    jumlah_siswa = Daftar_Siswa.objects.count()
    jumlah_kelas = Daftar_Kelas.objects.count()
    jumlah_wali = Daftar_Wali.objects.count()
    jumlah_prestasi = Daftar_Prestasi.objects.count()
    
    top_pelanggaran = (
        Poin_Pelanggaran.objects
        .select_related('pelanggaran')
        .values('pelanggaran__nama_pelanggaran')
        .annotate(total=Count('pelanggaran'))
        .order_by('-total')[:3]
    )
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
        'jumlah_kelas' : jumlah_kelas,
        'jumlah_wali' : jumlah_wali,
        'jumlah_prestasi' : jumlah_prestasi,
        'top_pelanggaran' : top_pelanggaran,
        'top_prestasi' : top_prestasi,
    }
    return render(request, 'beranda.html', context)


# ajax 
def load_nama_kelas(request):
    kelas_id = request.GET.get('kelas_id')
    nama_kelas = Daftar_Kelas.objects.filter(kelas=kelas_id).values('id', 'nama_kelas')
    return JsonResponse(list(nama_kelas), safe=False)

def load_nama_siswa(request):
    nama_kelas_id = request.GET.get('nama_kelas_id')
    siswa = Daftar_Siswa.objects.filter(kelas_id=nama_kelas_id).values('nisn', 'nama_siswa')
    return JsonResponse(list(siswa), safe=False)
# /ajax




# siswa
@login_required(login_url='HalamanLogin')
@ijinkan_pengguna(yang_diizinkan=['administrator']) 
def Daftar_Siswa_Ad(request):
    siswa = Daftar_Siswa.objects.all().order_by('-id')
    kategori_kelas = Daftar_Kelas.objects.all()
    tawa = Daftar_Wali.objects.all()
    context = {
        'judul' : 'Daftar Siswa',
        'menu' : 'datamaster',
        'submenu' : 'menusiswa',  
        'siswa' : siswa,
        'kategori_kelas' : kategori_kelas,
        'tawa' : tawa,
    }
    return render(request, 'daftar_siswa.html', context)

def tambah_siswa(request): 
    wali_kelas_list = Daftar_Wali.objects.all().order_by('-id')
    kelas_list = Daftar_Kelas.objects.all()
    
    if request.method == 'POST':
        nisn = request.POST.get('nisn')
        nama_siswa = request.POST.get('nama_siswa')
        kelas_id = request.POST.get('kelas')
        wali_kelas_id = request.POST.get('wali_kelas')
        
        kelas = Daftar_Kelas.objects.get(id=kelas_id)
        wali_kelas = Daftar_Wali.objects.get(id=wali_kelas_id)
        
        Daftar_Siswa.objects.create(
            nisn = nisn,
            nama_siswa = nama_siswa,
            kelas = kelas,
            wali_kelas = wali_kelas,
        )
        messages.success(request, f'{nama_siswa} Berhasil Ditambahkan')
        return redirect('Daftar_Siswa_Ad')

    context = {
        'judul' : 'tambah Siswa',
        'kelas_list' : kelas_list,
        'wali_kelas_list' : wali_kelas_list
    }
    return render(request, 'tambah_siswa.html', context)


def edit_siswa(request, id):
    siswa = get_object_or_404(Daftar_Siswa, id=id)

    if request.method == 'POST':
        siswa.nisn = request.POST.get('nisn')
        siswa.nama_siswa = request.POST.get('nama_siswa')
        siswa.save()
        messages.success(request, 'Berhasil Diperbarui')
        return redirect('Daftar_Siswa_Ad')
    
    context = {
        'siswa' : siswa,
    }
    
    return render(request, 'daftar_siswa.html', context)


def hapus_siswa(request,id): 
    siswa = get_object_or_404(Daftar_Siswa, id=id)
    siswa.delete()
    messages.success(request, 'Berhasil Dihapus')
    return redirect("Daftar_Siswa_Ad")

@login_required(login_url='HalamanLogin')
@ijinkan_pengguna(yang_diizinkan=['administrator']) 
def detail_siswa_ad(request, id):  
    siswa = get_object_or_404(Daftar_Siswa, id=id)
    mpelanggaran = Poin_Pelanggaran.objects.filter(siswa__nisn = siswa.nisn)
    mprestasi = Poin_Prestasi.objects.filter(siswa__nisn = siswa.nisn)
    
    context = {
        'judul' : 'Detail Siswa',
        'siswa' : siswa,
        'mpelanggaran' : mpelanggaran,
        'mprestasi' : mprestasi,
    }
    return render(request, 'detail_siswa_ad.html', context)

@login_required(login_url='HalamanLogin')
@ijinkan_pengguna(yang_diizinkan=['administrator']) 
def printpoin(request, siswa_id): 
    siswa = get_object_or_404(Daftar_Siswa, id=siswa_id)
    mpelanggaran = Poin_Pelanggaran.objects.filter(siswa=siswa)
    mprestasi = Poin_Prestasi.objects.filter(siswa=siswa)
    
        
    total_pelanggaran = mpelanggaran.aggregate(total_poin=Sum('pelanggaran__poin_pelanggaran'))['total_poin'] or 0
    total_prestasi = mprestasi.aggregate(total_poin=Sum('prestasi__poin_prestasi'))['total_poin'] or 0
        
    context = {
        'judul' : 'Print Poin',
        'siswa' : siswa,
        'mpelanggaran' : mpelanggaran,
        'mprestasi' : mprestasi,
        'total_pelanggaran' : total_pelanggaran,
        'total_prestasi' : total_prestasi,
    }
    return render(request, 'print.html', context)   
    
    return render(request, 'laporan.html', {'form' : LaporanForm()})



@login_required(login_url='HalamanLogin')
@ijinkan_pengguna(yang_diizinkan=['administrator']) 
def print_pelanggaran(request, id):
    mpelanggaran = get_object_or_404(Poin_Pelanggaran, id=id)
    siswa = mpelanggaran.siswa
    mprestasi = Poin_Prestasi.objects.filter(siswa=siswa)
    context = {
        'judul' : 'Print Poin',
        'siswa' : siswa,
        'mpelanggaran' : mpelanggaran,
        'mprestasi' : mprestasi,
    }
    return render(request, 'print_pelanggaran.html', context)
# /siswa




# wali kelas
@login_required(login_url='HalamanLogin')
@ijinkan_pengguna(yang_diizinkan=['administrator']) 
def Daftar_Wali_Ad(request):  
    tawa = Daftar_Wali.objects.all().order_by('-id')
    context = {
        'judul' : 'Daftar Wali Kelas',
        'menu' : 'datamaster',
        'submenu' : 'daftarwali',
        'tawa' : tawa,
        
    }
    return render(request, 'daftar_wali.html', context)


def tambah_wali(request):
    if request.method == 'POST':
        nip = request.POST['nip']
        nama_wali = request.POST['nama_wali']
        password = nip + 'wali'

        user = User.objects.create_user(username=nip, password=password)
        wali_kelas = Daftar_Wali(nip=nip, nama_wali=nama_wali, user=user)
        
        wali_kelas.save()
        user.save()
        
        group = Group.objects.get(name='walikelas')
        user.groups.add(group)
        messages.success(request, f'{nama_wali} Berhasil Ditambahkan sebagai wali kelas')
        return redirect("Daftar_Wali_Ad")
    else:
        return render(request, "daftar_wali.html")


def edit_wali(request, id):
    tawa = get_object_or_404(Daftar_Wali, id=id)
    if request.method == 'POST':
        nip = request.POST['nip']
        nama_wali = request.POST['nama_wali']
        
        tawa.nip = nip
        tawa.nama_wali = nama_wali
        
        user = tawa.user
        if user.username != nip:
            user.username = nip
            user.save()
            tawa.save()
            messages.success(request, 'berhasil Diperbarui ')
            return redirect('Daftar_Wali_Ad')
    
    return render (request, 'daftar_wali.html')

def hapus_wali(request,id):
    tawa = get_object_or_404(Daftar_Wali, id=id)
    
    if tawa.user:
        tawa.user.is_active = False
        tawa.user.save()
    
    tawa.delete()
    messages.success(request, 'Berhasil Dihapus')
    return redirect("Daftar_Wali_Ad")
# /wali kelas



# kelas
@login_required(login_url='HalamanLogin')
@ijinkan_pengguna(yang_diizinkan=['administrator']) 
def Kelas_Siswa_Ad(request):
    subquery = Daftar_Siswa.objects.filter(kelas=OuterRef('id')).values('kelas').annotate(
        jumlah_murid=Count('id')
    ).values('jumlah_murid')
    
    dakel = Daftar_Kelas.objects.annotate(
        jumlah_murid=Coalesce(Subquery(subquery), 0)
    ).order_by('-id')
    kelas = Daftar_Wali.objects.all().order_by('-id')
    context = {
        'judul' : 'Daftar Kelas',
        'menu' : 'datamaster',
        'submenu' : 'menukelas',
        'kelas' : kelas,
        'dakel' : dakel,
    }
    return render(request, 'daftar_kelas.html', context)

def detail_siswa_kelas(request, kelas_id):
    kelas = get_object_or_404(Daftar_Kelas, id=kelas_id)
    siswa_list = Daftar_Siswa.objects.filter(kelas=kelas)
    kelas_list = Daftar_Kelas.objects.exclude(id=kelas_id)
    context = {
        'kelas' : kelas,
        'siswa_list' : siswa_list,
        'kelas_list' : kelas_list,
    }
    return render(request, 'daftar_siswa_kelas.html', context)


def promote_class(request):
    if request.method == 'POST':
        kelas_id = request.POST.get('kelas_id') #ambil ID kelas saat ini
        kelas_baru_id = request.POST.get('kelas_baru_id') #ambil ID kelas baru
        
        kelas_baru = get_object_or_404(Daftar_Kelas, id=kelas_baru_id) #ambil objek kelas baru
        
        siswa_ids = request.POST.getlist('select_siswa') #ambil ID siswa yang dipilih
        
        if siswa_ids: #jika ada siswa yang dipilih , perbarui kelas mereka
            Daftar_Siswa.objects.filter(id__in=siswa_ids).update(kelas=kelas_baru)
            messages.success(request, 'Kelas siswa berhasil diperbarui.')
        else:
            messages.error(request, 'Tidak ada siswa yang dipilih')

        return redirect('detail_siswa_kelas', kelas_id=kelas_baru_id)
    return redirect('detail_siswa_kelas')
    

def tambah_kelas(request):
    kelas = Daftar_Wali.objects.all().order_by('-id')
    context = {
        'judul' : 'tambah kelas',
        'menu' : 'tambah kelas',
        'kelas' : kelas,
    }
    return render(request, 'tambah_kelas.html', context)

def takel(request):
    if request.method == 'POST':
        a = request.POST['kelas']
        b = request.POST['nama_kelas']
        c = request.POST['wali_kelas']
        
        try:
            wali_kelas_obj = Daftar_Wali.objects.get(id=c)
        except Daftar_Wali.DoesNotExist:
            messages.error(request, 'wali kelas yang dipilih tidak ditemukan')
            return redirect("Kelas_Siswa_Ad")
        
        dakel = Daftar_Kelas(kelas = a, nama_kelas = b, wali_kelas=wali_kelas_obj)
        dakel.save()
        messages.success(request, f"{a} - {b} Berhasil Ditambahkan")
        return redirect("Kelas_Siswa_Ad")
    semua_wali_kelas = Daftar_Wali.objects.all()
    return render(request, 'daftar_kelas.html', {'kelas' : semua_wali_kelas})

def edit_kelas(request, id):
    dakel = get_object_or_404(Daftar_Kelas, id=id)
    if request.method == 'POST':
        dakel.kelas = request.POST['kelas']
        dakel.nama_kelas = request.POST['nama_kelas']
        
        
        wali_kelas_id = request.POST['wali_kelas']
        dakel.wali_kelas = Daftar_Wali.objects.filter(id=wali_kelas_id).first()
        dakel.save()
        messages.success(request, 'berhasil Diperbarui ')
        return redirect('Kelas_Siswa_Ad')
    
    context = {
        'dakel' : dakel,
        'kelas' : Daftar_Kelas.objects.all()
    }
    return render (request, 'daftar_kelas.html', context)

def hapus_kelas(request,id): # delete kelas
    dakel = get_object_or_404(Daftar_Kelas, id=id)
    dakel.delete()
    messages.success(request, 'Berhasil Dihapus')
    return redirect("Kelas_Siswa_Ad")
# /kelas


# pelanggaran
@login_required(login_url='HalamanLogin')
@ijinkan_pengguna(yang_diizinkan=['administrator']) 
def daftar_pelanggaran_ad(request): 
    dapel = Daftar_Pelanggaran.objects.all().order_by('-id')  
    context = {
        'menu': 'pelanggaransiswa',
        'submenu': 'daftarpelanggaran',
        'judul' : 'Daftar Pelanggaran',
        'dapel' : dapel,
        }
    return render(request, 'daftar_pelanggaran.html', context)

def tambah_dapel(request):
    if request.method == 'POST':
        f = request.POST['napel']
        g = request.POST['jumpo']
        dapel = Daftar_Pelanggaran(nama_pelanggaran = f, poin_pelanggaran = g)
        dapel.save()
        messages.success(request, f'{f} Berhasil Ditambahkan')
        return redirect("daftar_pelanggaran_ad")
    return render(request, "daftar_pelanggaran.html")

def hapus_dapel(request,id):
    dapel = get_object_or_404(Daftar_Pelanggaran, id=id)
    dapel.delete()
    messages.success(request, 'Berhasil Dihapus')
    return redirect("daftar_pelanggaran_ad")

def edit_pelanggaran(request, id):
    dapel = Daftar_Pelanggaran.objects.get(id=id)
    if request.method == 'POST':
        dapel.nama_pelanggaran = request.POST['napel']
        dapel.poin_pelanggaran = request.POST['jumpo']
        dapel.save()
        messages.success(request, 'berhasil Diperbarui ')
        return redirect('daftar_pelanggaran_ad')
    
    context = {
        'dapel' : dapel,
    }
    return render (request, 'daftar_pelanggaran.html', context)

@login_required(login_url='HalamanLogin')
@ijinkan_pengguna(yang_diizinkan=['administrator']) 
def poin_pelanggaran_ad(request):
    mpelanggaran = Poin_Pelanggaran.objects.all().order_by("-id")
    context = {
        'menu': 'pelanggaransiswa', 
        'submenu': 'poinpelanggaran',
        'judul' : 'Poin Pelanggaran',
        'mpelanggaran' : mpelanggaran,
        }
    return render(request, 'poin_pelanggaran.html', context)
# /pelanggaran


# prestasi
@login_required(login_url='HalamanLogin')
@ijinkan_pengguna(yang_diizinkan=['administrator']) 
def daftar_prestasi_ad(request):
    pres = Daftar_Prestasi.objects.all().order_by('-id')
    context = {
        'judul' : 'Daftar Prestasi',
        'submenu': 'daftarprestasik',
        'menu' : 'DaftarPrestasi',
        'pres' : pres,
    }
    return render(request, 'daftar_prestasi.html', context)

def tambah_daftar_pre(request):
    if request.method == 'POST':
        h = request.POST['napre']
        i = request.POST['jumpre']
        pres = Daftar_Prestasi(nama_prestasi = h, poin_prestasi = i)
        pres.save()
        messages.success(request, f'{h} Berhasil Ditambahkan')
        return redirect("daftar_prestasi_ad")
    return render(request, "daftar_prestasi.html")

def edit_prestasi(request, id):
    pres = Daftar_Prestasi.objects.get(id=id)
    if request.method == 'POST':
        pres.nama_prestasi = request.POST['napre']
        pres.poin_prestasi = request.POST['jumpre']
        pres.save()
        messages.success(request, 'berhasil Diperbarui ')
        return redirect('daftar_prestasi_ad')
    
    context = {
        'pres' : pres,
    }
    return render (request, 'daftar_prestasi.html', context)

def hapus_prestasi(request,id):
    pres = get_object_or_404(Daftar_Prestasi, id=id)
    pres.delete()
    messages.success(request, 'Berhasil Dihapus')
    return redirect("daftar_prestasi_ad")

@login_required(login_url='HalamanLogin')
@ijinkan_pengguna(yang_diizinkan=['administrator']) 
def poin_prestasi_ad(request):
    mprestasi = Poin_Prestasi.objects.all().order_by('-id')
    context = {
        'judul' : 'Poin Prestasi',
        'submenu': 'poinprestasi',
        'menu' : 'DaftarPrestasi',
        'mprestasi' : mprestasi,
    }
    return render(request, 'poin_prestasi.html', context)
# /prestasi


# laporan
@login_required(login_url='HalamanLogin')
@ijinkan_pengguna(yang_diizinkan=['administrator']) 
def laporan_view(request):
    mpelanggaran = Daftar_Pelanggaran.objects.all()
    mprestasi = Daftar_Prestasi.objects.all()
    if request.method == "POST":
        form = LaporanForm(request.POST)
        if form.is_valid():
            siswa = form.cleaned_data['siswa']
            tanggal_mulai = form.cleaned_data['tanggal_mulai']
            tanggal_selesai = form.cleaned_data['tanggal_selesai']
            
            mpelanggaran = Poin_Pelanggaran.objects.filter(
                siswa__nisn = siswa.nisn,
                waktu__range=[tanggal_mulai, tanggal_selesai]
            )
            mprestasi = Poin_Prestasi.objects.filter(
                siswa__nisn = siswa.nisn,
                waktu_prestasi__range=[tanggal_mulai, tanggal_selesai]
            )
            
            total_pelanggaran = sum(p.pelanggaran.poin_pelanggaran for p in mpelanggaran)
    
            total_prestasi = sum(p.prestasi.poin_prestasi for p in mprestasi)

            context = {
                'form' : form,
                'siswa' : siswa,
                'mpelanggaran' : mpelanggaran,
                'mprestasi' : mprestasi,
                'total_pelanggaran' : total_pelanggaran,
                'total_prestasi' : total_prestasi,
            }
            return render(request, 'laporan.html', context)
    else:
        form = LaporanForm()
        
    return render(request, 'laporan.html', {'form':form})
# /laporan

