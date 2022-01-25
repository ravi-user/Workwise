# Generated by Django 3.2.7 on 2021-12-25 15:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Seeker', '0012_jcomment'),
    ]

    operations = [
        migrations.CreateModel(
            name='Link',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('facebook', models.CharField(max_length=100)),
                ('twitter', models.CharField(max_length=100)),
                ('pinterest', models.CharField(max_length=100)),
                ('instagram', models.CharField(max_length=100)),
                ('youtube', models.CharField(max_length=100)),
                ('seeker_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Seeker.seeker')),
            ],
        ),
    ]