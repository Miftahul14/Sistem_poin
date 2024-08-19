from typing import Any
from django import forms
from .models import *
from django_select2.forms import Select2Widget


class LaporanForm(forms.Form):
    siswa = forms.ModelChoiceField(
        queryset=Daftar_Siswa.objects.all(),
        label='Nama Siswa',
        widget=Select2Widget(attrs={'class' : 'form-control custom-select'})
    )
    
    tanggal_mulai = forms.DateField(
        widget=forms.SelectDateWidget(attrs={'class' : 'form-control date-input'}), 
        label='dari tanggal'
    )
    
    tanggal_selesai = forms.DateField(
        widget=forms.SelectDateWidget(attrs={'class' : 'form-control date-input'}), 
        label='sampai tanggal'
    )
    

