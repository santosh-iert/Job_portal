# Generated by Django 4.2.17 on 2024-12-18 16:53

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PostedJobs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('job_title', models.CharField(max_length=20, unique=True)),
                ('job_description', models.TextField()),
                ('posted_date', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(choices=[('ACTIVE', 'active'), ('CLOSED', 'closed')], default='ACTIVE', max_length=20)),
            ],
            options={
                'ordering': ['-posted_date'],
            },
        ),
    ]