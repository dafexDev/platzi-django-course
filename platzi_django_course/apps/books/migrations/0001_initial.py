# Generated by Django 5.1.3 on 2024-11-29 19:32

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=200)),
                ('birth_date', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Publisher',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=200)),
                ('address', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='AuthorProfile',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('website', models.URLField(blank=True, null=True)),
                ('biography', models.TextField(blank=True, max_length=500, null=True)),
                ('author', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to='books.author')),
            ],
        ),
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=200)),
                ('publication_date', models.DateField()),
                ('authors', models.ManyToManyField(related_name='books', to='books.author')),
                ('publisher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='books.publisher')),
            ],
        ),
    ]