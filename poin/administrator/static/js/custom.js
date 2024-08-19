// alert tambah data
$(document).ready(function() {
    var successMessage = $('.alert-success').data('message');
    if (successMessage) {
        Swal.fire({
            icon: 'success',
            title: 'Sukses',
            text: successMessage,
            timer: 3000,
            showConfirmButton: false
        });
    }

    var errorMessage = $('.alert-danger').data('message');
    if (errorMessage) {
        Swal.fire({
            icon: 'error',
            title: 'Error',
            text: errorMessage,
            timer: 3000,
            showConfirmButton: false
        });
    }
});

// alert tambah data

// js detail poin pelanggaran
$('#detailpoinpelanggaransiswa').on('show.bs.modal', function (event) {
    var button = $(event.relatedTarget); 
    var nama = button.data('nama');
    var kelas = button.data('kelas');
    var kategori = button.data('kategori');
    var poin = button.data('poin');
    var waktu = button.data('waktu');
    var keterangan = button.data('keterangan');

    var modal = $(this);
    modal.find('#modal-nama-siswa').val(nama);
    modal.find('#modal-kelas-siswa').val(kelas);
    modal.find('#modal-kelas-kategori').val(kategori);
    modal.find('#modal-poin-siswa').val(poin);
    modal.find('#modal-waktu-siswa').val(waktu);
    modal.find('#modal-keterangan-siswa').val(keterangan);
});
// js detail poin pelanggaran


// js detail poin prestasi
$('#detailpoinprestasisiswa').on('show.bs.modal', function (event) {
    var button = $(event.relatedTarget); 
    var nama = button.data('nama');
    var kelas = button.data('kelas');
    var kategori_admin = button.data('kategori_admin');
    var waktu = button.data('waktu');
    var keterangan = button.data('keterangan');

    var modal = $(this);
    modal.find('#modal-nama').val(nama);
    modal.find('#modal-kelas').val(kelas);
    modal.find('#modal-kategori_admin').val(kategori_admin);
    modal.find('#modal-waktu').val(waktu);
    modal.find('#modal-keterangan').val(keterangan);
});
// js detail poin prestasi


// js daftar guru
$('#detaildaftarguruad').on('show.bs.modal', function (event) {
    var tombol = $(event.relatedTarget); 
    var nuptk = tombol.data('nuptk');
    var namaGuru = tombol.data('nama');
    var mataPelajaran = tombol.data('mapel');

    var modal = $(this);
    modal.find('#modal-nuptk').val(nuptk);
    modal.find('#modal-nama').val(namaGuru);
    modal.find('#modal-mapel').val(mataPelajaran);
});


// js daftar guru


