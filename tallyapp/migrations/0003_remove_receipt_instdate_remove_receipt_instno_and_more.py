# Generated by Django 4.0.4 on 2022-06-26 10:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tallyapp', '0002_receipt'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='receipt',
            name='instdate',
        ),
        migrations.RemoveField(
            model_name='receipt',
            name='instno',
        ),
        migrations.RemoveField(
            model_name='receipt',
            name='transactiontype',
        ),
        migrations.CreateModel(
            name='receiptbank',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('instno', models.IntegerField()),
                ('instdate', models.DateField()),
                ('amount', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tallyapp.particulars')),
                ('date', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tallyapp.account')),
                ('ledger', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tallyapp.ledger')),
                ('transactiontype', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tallyapp.transactiontype')),
            ],
        ),
    ]
