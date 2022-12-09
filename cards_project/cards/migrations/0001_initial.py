# Generated by Django 3.2.16 on 2022-12-09 15:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Card',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('series', models.IntegerField(verbose_name='Серия карты')),
                ('number', models.IntegerField(verbose_name='Номер карты')),
                ('type', models.CharField(choices=[('карта лояльности', 'loyalty'), ('подарочная карта', 'gift'), ('кредитная карта', 'credit')], default='подарочная карта', max_length=100, verbose_name='Тип карты')),
                ('issue_date', models.DateTimeField(verbose_name='Дата выпуска')),
                ('validity_period', models.CharField(choices=[('short period', '3 месяца'), ('middle period', '6 месяцев'), ('long period', '12 месяцев')], default='short period', max_length=100, verbose_name='Срок действия карты')),
                ('activity_end_date', models.DateTimeField(verbose_name='Дата окончания активности карты')),
                ('status', models.CharField(choices=[('активирована', 'active'), ('не активирована', 'not active'), ('просрочена', 'expired')], default='не активирована', max_length=100, verbose_name='Статус карты')),
                ('payout', models.IntegerField(verbose_name='Сумма на карте')),
            ],
            options={
                'verbose_name': 'Карта',
                'verbose_name_plural': 'Карты',
            },
        ),
        migrations.CreateModel(
            name='Purchase',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(verbose_name='Дата и время покупки')),
                ('price', models.IntegerField(verbose_name='Сумма покупки')),
            ],
            options={
                'verbose_name': 'Покупка',
                'verbose_name_plural': 'Покупки',
            },
        ),
        migrations.CreateModel(
            name='Operation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('card', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cards.card', verbose_name='Карта, которой оплачена покупка')),
                ('purchase', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cards.purchase', verbose_name='Данные о покупке')),
            ],
            options={
                'verbose_name': 'Операция по карте',
                'verbose_name_plural': 'Операции по карте',
            },
        ),
        migrations.AddField(
            model_name='card',
            name='usage',
            field=models.ManyToManyField(blank=True, through='cards.Operation', to='cards.Purchase', verbose_name='Дата и время использования'),
        ),
    ]
