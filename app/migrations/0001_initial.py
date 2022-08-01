# Generated by Django 2.2.2 on 2019-06-21 00:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Bid',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bid_status', models.BooleanField(default=False)),
                ('bid_created', models.DateTimeField(auto_now_add=True)),
                ('bid_modified', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company_name', models.CharField(max_length=255)),
                ('company_address', models.CharField(max_length=255)),
                ('company_description', models.TextField(default='There is currently no description available for this company.')),
                ('company_created', models.DateTimeField(auto_now_add=True)),
                ('company_modified', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Placement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('placement_title', models.CharField(max_length=255)),
                ('placement_slug', models.SlugField()),
                ('placement_created', models.DateTimeField(auto_now_add=True)),
                ('placement_modified', models.DateTimeField(auto_now=True)),
                ('placement_company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Company')),
            ],
        ),
        migrations.CreateModel(
            name='PlacementBid',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('offer', models.IntegerField()),
                ('shares', models.IntegerField()),
                ('confirmed', models.BooleanField(default=False)),
                ('placementbid_created', models.DateTimeField(auto_now_add=True)),
                ('placementbid_modified', models.DateTimeField(auto_now=True)),
                ('bid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Bid')),
                ('placement', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Placement')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
