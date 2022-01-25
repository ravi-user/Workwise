# Generated by Django 3.2.7 on 2021-11-29 10:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Company', '0003_delete_job'),
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cname', models.CharField(max_length=50, unique=True)),
                ('city', models.CharField(max_length=20)),
                ('id_proof', models.FileField(upload_to='media/documents')),
                ('c_pic', models.FileField(upload_to='media/images')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Company.user')),
            ],
        ),
    ]
