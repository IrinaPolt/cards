from django.db import models


class Purchase(models.Model):
    date = models.DateTimeField(
        verbose_name='Дата и время покупки'
    )
    price = models.IntegerField(
        verbose_name='Сумма покупки'
    )

    class Meta:
        verbose_name='Покупка'
        verbose_name_plural='Покупки'


class Card(models.Model):
    # константы для систематизации карт

    LOYALTY = 'карта лояльности'
    GIFT = 'подарочная карта'
    CREDIT = 'кредитная карта'

    TYPE_CHOCES = (
        (LOYALTY, 'loyalty'),
        (GIFT, 'gift'),
        (CREDIT, 'credit')
    )

    ACTIVE = 'активирована'
    N_ACTIVE = 'не активирована'
    EXPIRED = 'просрочена'

    STATUS_CHOICES = (
        (ACTIVE, 'active'),
        (N_ACTIVE, 'not active'),
        (EXPIRED, 'expired')
    )

    SHORT = 'short period'
    MIDDLE = 'middle period'
    LONG = 'long period'

    PERIOD_CHOICES = (
        (SHORT, '3 месяца'),
        (MIDDLE, '6 месяцев'),
        (LONG, '12 месяцев')
    )

    series = models.IntegerField(
        verbose_name='Серия карты'
    )
    number = models.IntegerField(
        verbose_name='Номер карты'
    )
    type = models.CharField(
        verbose_name='Тип карты',
        max_length=100,
        choices=TYPE_CHOCES,
        default=GIFT
    )
    issue_date = models.DateTimeField(
        verbose_name='Дата выпуска'
    )
    validity_period = models.CharField(
        max_length=100,
        choices=PERIOD_CHOICES,
        default=SHORT,
        verbose_name='Срок действия карты'
    )
    activity_end_date = models.DateTimeField(
        verbose_name='Дата окончания активности карты'
    )
    status = models.CharField(
        max_length=100,
        choices=STATUS_CHOICES,
        default=N_ACTIVE,
        verbose_name='Статус карты'
    )
    usage = models.ManyToManyField(
        Purchase,
        through='Operation',
        verbose_name='Дата и время использования',
        blank=True
    )
    payout = models.IntegerField(
        verbose_name='Сумма на карте'
    )

    class Meta:
        verbose_name='Карта'
        verbose_name_plural='Карты'
    
    def __str__(self):
        return f'Карта {self.series} {self.number}'


class Operation(models.Model):
    card = models.ForeignKey(
        Card,
        on_delete=models.CASCADE,
        verbose_name='Карта, которой оплачена покупка'
    )
    purchase = models.ForeignKey(
        Purchase,
        on_delete=models.CASCADE,
        verbose_name='Данные о покупке'
    )

    class Meta:
        verbose_name='Операция по карте'
        verbose_name_plural='Операции по карте'
