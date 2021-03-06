# Generated by Django 3.0.4 on 2021-06-30 15:01

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Bibliografia',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dni', models.CharField(max_length=50)),
                ('author', models.CharField(max_length=50, null=True)),
                ('title', models.CharField(max_length=50, null=True)),
                ('keyword', models.CharField(max_length=50, null=True)),
                ('description', models.CharField(max_length=200, null=True)),
                ('memoir', models.FileField(max_length=200, null=True, upload_to='')),
                ('id_folder', models.CharField(max_length=50, null=True)),
                ('tutor', models.CharField(max_length=50, null=True)),
                ('cotutor', models.CharField(max_length=50, null=True)),
                ('readed', models.BooleanField(default=False, null=True)),
                ('uploaded', models.BooleanField(default=False, null=True)),
                ('authorized_by_author', models.BooleanField(default=False, null=True)),
                ('upload_hour', models.CharField(max_length=50, null=True)),
                ('upload_date', models.CharField(max_length=50, null=True)),
                ('first_court_member', models.CharField(max_length=50, null=True)),
                ('second_court_member', models.CharField(max_length=50, null=True)),
                ('third_court_member', models.CharField(max_length=50, null=True)),
                ('admin_documentation', models.BooleanField(default=False, null=True)),
                ('admin_record', models.BooleanField(default=False, null=True)),
                ('year', models.CharField(max_length=50, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Profesor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('departure', models.CharField(max_length=50)),
                ('area', models.CharField(max_length=50)),
                ('email', models.CharField(max_length=50)),
            ],
        ),
    ]
