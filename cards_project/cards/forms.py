from django import forms

from .models import STATUS_CHOICES, Card


class CardForm(forms.ModelForm):
    payout = forms.IntegerField(initial=0)
    amount = forms.IntegerField(required=False)
    status = forms.ChoiceField(choices=STATUS_CHOICES, required=False)

    class Meta:
        model = Card
        fields = (
            'series',
            'type',
            'validity_period',
            'payout',
            'status'
        )
