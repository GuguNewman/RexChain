# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-10-01 18:20
from __future__ import unicode_literals

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('public_key_b64', models.TextField(default=b'', help_text=b'Format: Base 64', unique=True, verbose_name=b'Public Key')),
                ('address', models.CharField(default=b'', help_text=b'Format: Base 58 and valid bitcoin address', max_length=255, verbose_name=b'Address to get transactions')),
                ('is_valid', models.BooleanField(default=True, verbose_name=b'Check if address is valid')),
            ],
            options={
                'ordering': ['created_at'],
                'verbose_name_plural': 'Valid Bitcoin Addresses',
            },
        ),
        migrations.CreateModel(
            name='Block',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hash_block', models.CharField(blank=True, default=b'', max_length=255)),
                ('previous_hash', models.CharField(blank=True, default=b'', max_length=255)),
                ('timestamp', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('data', django.contrib.postgres.fields.jsonb.JSONField(blank=True, default={})),
                ('merkleroot', models.CharField(default=b'', max_length=255)),
                ('poetxid', models.CharField(blank=True, default=b'', max_length=255)),
                ('nonce', models.CharField(blank=True, default=b'', max_length=50)),
                ('hashcash', models.CharField(blank=True, default=b'', max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Medication',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('active', models.TextField(blank=True, default=b'')),
                ('presentation', models.TextField(blank=True, default=b'')),
                ('instructions', models.TextField(blank=True, default=b'')),
                ('frequency', models.TextField(blank=True, default=b'')),
                ('dose', models.TextField(blank=True, default=b'')),
                ('bought', models.BooleanField(default=False)),
                ('drug_upc', models.TextField(blank=True, db_index=True, default=b'')),
            ],
        ),
        migrations.CreateModel(
            name='Prescription',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('timestamp', models.DateTimeField(blank=True, default=django.utils.timezone.now, verbose_name=b'Datetime object')),
                ('readable', models.BooleanField(default=False, verbose_name=b'Check if data is readable(synonym spent)')),
                ('is_valid', models.BooleanField(default=True, verbose_name=b'Check if signature validation was valid')),
                ('hash_id', models.TextField(blank=True, default=b'', verbose_name=b'Hash for Blockchainize Object')),
                ('previous_hash', models.TextField(blank=True, default=b'0', verbose_name=b'Previous Hash for Blockchainize Object')),
                ('raw_msg', models.TextField(blank=True, default=b'', verbose_name=b'Chaining raw data of Blockchainize object for hashing purpose')),
                ('data', django.contrib.postgres.fields.jsonb.JSONField(blank=True, default={}, verbose_name=b'Raw Data from Payload')),
                ('public_key', models.TextField(blank=True, default=True, verbose_name=b'An Hex representation of Public Key Object')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(db_index=True, default=django.utils.timezone.now)),
                ('raw_msg', models.TextField(blank=True, default=b'')),
                ('signature', models.TextField(blank=True, default=b'')),
                ('is_valid', models.BooleanField(default=False)),
                ('txid', models.TextField(blank=True, default=b'')),
                ('previous_hash', models.TextField(blank=True, default=b'')),
                ('details', django.contrib.postgres.fields.jsonb.JSONField(blank=True, default={})),
                ('block', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='transactions', to='blockchain.Block')),
            ],
        ),
        migrations.AddField(
            model_name='prescription',
            name='transaction',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='prescriptions', to='blockchain.Transaction'),
        ),
        migrations.AddField(
            model_name='medication',
            name='prescription',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='medications', to='blockchain.Prescription'),
        ),
    ]