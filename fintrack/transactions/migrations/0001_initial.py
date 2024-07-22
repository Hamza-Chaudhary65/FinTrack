# Generated by Django 4.2.13 on 2024-07-22 09:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField(blank=True)),
                ('category', models.CharField(choices=[('WITHDRAW', 'Withdraw'), ('DEPOSIT', 'Deposit')], max_length=20)),
                ('date', models.DateField()),
                ('amount', models.IntegerField()),
                ('transaction_from_account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transactions', to='accounts.account')),
            ],
        ),
    ]
