# Generated by Django 5.0.7 on 2024-07-23 09:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gurubk', '0004_remove_poin_pelanggaran_kategori_kelas_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='poin_pelanggaran',
            name='kategori_kelas',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='poin_pelanggaran',
            name='nama_kelas',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]
