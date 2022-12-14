import random
import string
import datetime
from django.db.models import Q
from django.views.generic import ListView, TemplateView
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Card, Operation, ACTIVE, GIFT, LOYALTY, CREDIT
from .forms import CardForm


def count_end_date(date, period):
    if period == '1 месяц':
        return date + datetime.timedelta(days=31)
    elif period == '6 месяцев':
        return date + datetime.timedelta(days=92)
    else:
        return date + datetime.timedelta(days=365)


class IndexView(TemplateView):
    template_name = 'cards/index.html'

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)


@login_required
def card_edit(request, card_id):
    card = get_object_or_404(Card, pk=card_id)
    operations = Operation.objects.filter(card=card)
    old_status = card.status
    old_validity_period = card.validity_period
    form = CardForm(request.POST or None, instance=card)
    if form.is_valid():
        new_status = form.data['status']
        new_validity_period = form.data['validity_period']
        form.save()
        if new_status == 'просрочена' and old_status != new_status:
            card.activity_end_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        if new_validity_period != old_validity_period:
            card.activity_end_date=count_end_date(card.issue_date, new_validity_period)
        card.save()
        return redirect('cards:index')
    return render(request, 'cards/single_card.html',
                          {'form': form, 'card_id': card_id, 'operations': operations})


@login_required
def card_delete(request, card_id):
    card = get_object_or_404(Card, pk=card_id)
    card.delete()
    return HttpResponseRedirect(reverse('cards:index'))


@login_required
def show_gift(request):
    type = GIFT
    cards = Card.objects.filter(type=type)
    context = {
        'cards': cards,
        'type': type,
    }
    return render(request, 'cards/show_cards.html', context)


@login_required
def show_loyalty(request):
    type = LOYALTY
    cards = Card.objects.filter(type=type)
    context = {
        'cards': cards,
        'type': type,
    }
    return render(request, 'cards/show_cards.html', context)


@login_required
def show_credit(request):
    type = CREDIT
    cards = Card.objects.filter(type=type)
    context = {
        'cards': cards,
        'type': type,
    }
    return render(request, 'cards/show_cards.html', context)


@login_required
def create_cards(request):
    N = 6 # amount of digits in a card number
    print(request)
    if request.method == 'POST':
        form = CardForm(request.POST)
        print(form.data)
        if form.is_valid():
            amount = form.data['amount']
            for _ in range(int(amount)):
                Card.objects.create(
                    series=form.data['series'],
                    number=''.join(random.choices(string.digits, k=N)),
                    type=form.data['type'],
                    issue_date=datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
                    validity_period=form.data['validity_period'],
                    activity_end_date=count_end_date(datetime.datetime.now(), form.data['validity_period']),
                    status=ACTIVE,
                    payout=form.data['payout'],
                )
            return HttpResponseRedirect(reverse('cards:index'))
        else:
            form = CardForm()
        context = {
            'form': form,
        }
        return render(request, 'cards/create_card.html', context)
    else:
        form = CardForm()
        context = {
            'form': form,
        }
        return render(request, 'cards/create_card.html', context)


class SearchView(ListView):
    model = Card
    template_name = 'cards/search_results.html'

    def get_queryset(self):
        query = self.request.GET.get('q')
        object_list = Card.objects.filter(
            Q(series__icontains=query) |
            Q(number__icontains=query) |
            Q(type__icontains=query) |
            Q(status__icontains=query) |
            Q(issue_date__icontains=query) |
            Q(activity_end_date__icontains=query) |
            Q(status__icontains=query)
        )
        return object_list
