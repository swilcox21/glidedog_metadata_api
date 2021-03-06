# Generated by Django 4.0 on 2022-02-03 22:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Dataset',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('owner', models.CharField(max_length=50)),
                ('version', models.IntegerField(default=1)),
                ('current', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Table',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('rows', models.IntegerField()),
                ('version', models.IntegerField(default=1)),
                ('current', models.BooleanField(default=True)),
                ('dataset', models.ManyToManyField(related_name='table', to='api.Dataset')),
            ],
        ),
        migrations.CreateModel(
            name='Column',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('type', models.CharField(max_length=50)),
                ('rows', models.IntegerField()),
                ('table', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='column', to='api.table')),
            ],
        ),
    ]
