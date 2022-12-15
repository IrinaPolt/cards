import datetime

from django.db import models

# константы для систематизации карт

LOYALTY = 'карты лояльности'
GIFT = 'подарочные карты'
CREDIT = 'кредитные карты'

TYPE_CHOICES = (
    (LOYALTY, 'карта лояльности'),
    (GIFT, 'подарочная карта'),
    (CREDIT, 'кредитная карта')
)

ACTIVE = 'активирована'
N_ACTIVE = 'не активирована'
EXPIRED = 'просрочена'

STATUS_CHOICES = (
    (ACTIVE, 'active'),
    (N_ACTIVE, 'not active'),
    (EXPIRED, 'expired')
)

SHORT = '1 месяц'
MIDDLE = '6 месяцев'
LONG = '12 месяцев'

PERIOD_CHOICES = (
    (SHORT, '1 месяц'),
    (MIDDLE, '6 месяцев'),
    (LONG, '1 год')
)


class Purchase(models.Model):
    date = models.DateTimeField(
        verbose_name='Дата и время покупки'
    )
    price = models.IntegerField(
        verbose_name='Сумма покупки'
    )

    class Meta:
        verbose_name = 'Покупка'
        verbose_name_plural = 'Покупки'


class Card(models.Model):

    series = models.IntegerField(
        verbose_name='Серия карты'
    )
    number = models.IntegerField(
        verbose_name='Номер карты'
    )
    type = models.CharField(
        verbose_name='Тип карты',
        max_length=100,
        choices=TYPE_CHOICES,
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
        verbose_name='Сумма на карте',
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = 'Карта'
        verbose_name_plural = 'Карты'

    def __str__(self):
        return f'Карта {self.series} {self.number}'

    def check_status(self):
        now = datetime.datetime.now()
        if now > self.activity_end_date and self.status == ACTIVE:
            self.status = N_ACTIVE
            self.save()
            return N_ACTIVE
        return ACTIVE


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
        verbose_name = 'Операция по карте'
        verbose_name_plural = 'Операции по карте'
