# Generated by Django 5.0.7 on 2024-08-07 02:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('walikelas', '0003_alter_poin_prestasi_prestasi'),
    ]

    operations = [
        migrations.AlterField(
            model_name='poin_prestasi',
            name='prestasi',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
