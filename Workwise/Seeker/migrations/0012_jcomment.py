# Generated by Django 3.2.7 on 2021-12-21 08:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Seeker', '0011_comment'),
    ]

    operations = [
        migrations.CreateModel(
            name='Jcomment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(max_length=100)),
                ('job_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Seeker.job')),
                ('seeker_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Seeker.seeker')),
            ],
        ),
    ]
