# Generated by Django 4.0.3 on 2024-03-28 08:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PostOffice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('address', models.CharField(max_length=200)),
                ('zip_code', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Package',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('destination_address', models.CharField(max_length=200)),
                ('destination_zip_code', models.CharField(max_length=20)),
                ('recipient_name', models.CharField(max_length=100)),
                ('tracking_number', models.CharField(max_length=50, unique=True)),
                ('package_type', models.CharField(choices=[('Letter', 'Letter'), ('Package', 'Package')], max_length=10)),
                ('status', models.CharField(default='Registered', max_length=100)),
                ('history', models.JSONField(default=list)),
                ('destination_office', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='destination_packages', to='shortenurl.postoffice')),
                ('intermediate_office', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='intermediate_packages', to='shortenurl.postoffice')),
                ('origin_office', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='origin_packages', to='shortenurl.postoffice')),
            ],
        ),
    ]
