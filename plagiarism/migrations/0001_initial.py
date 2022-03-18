# Generated by Django 4.0.3 on 2022-03-18 10:38

from django.db import migrations, models
import django.db.models.deletion
import plagiarism.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('name', models.CharField(max_length=100, null=True)),
                ('email', models.CharField(max_length=100, unique=True)),
                ('username', models.CharField(max_length=50, null=True, unique=True)),
                ('password', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
            ],
            options={
                'db_table': 'users',
            },
        ),
        migrations.CreateModel(
            name='Golongan',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nama', models.CharField(max_length=10, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
            ],
            options={
                'db_table': 'golongan',
            },
        ),
        migrations.CreateModel(
            name='MataKuliah',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nama', models.CharField(max_length=100, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
            ],
            options={
                'db_table': 'mata_kuliah',
            },
        ),
        migrations.CreateModel(
            name='LearningJurnal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.CharField(max_length=100, null=True)),
                ('nama', models.CharField(max_length=100, null=True)),
                ('nim', models.CharField(max_length=10, null=True)),
                ('semester', models.SmallIntegerField(choices=[('SATU', 1), ('DUA', 2), ('TIGA', 3), ('EMPAT', 4), ('LIMA', 5), ('ENAM', 6), ('TUJUH', 7), ('DELAPAN', 8)], default=plagiarism.models.Semester['SATU'], null=True)),
                ('golongan', models.CharField(max_length=2, null=True)),
                ('minggu', models.SmallIntegerField(null=True)),
                ('tanggal_perkuliahan', models.DateField(null=True)),
                ('topik', models.CharField(max_length=255, null=True)),
                ('pembahasan', models.TextField(null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('matkul', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='plagiarism.matakuliah')),
            ],
            options={
                'db_table': 'learning_jurnal',
            },
        ),
    ]