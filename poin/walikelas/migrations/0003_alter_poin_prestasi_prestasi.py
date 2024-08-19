# Generated by Django 5.0.7 on 2024-08-07 02:04

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('administrator', '0005_daftar_wali_user'),
        ('walikelas', '0002_remove_poin_prestasi_kategori_kelas_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='poin_prestasi',
            name='prestasi',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='poin_prestasi_wali', to='administrator.daftar_prestasi'),
        ),
    ]
