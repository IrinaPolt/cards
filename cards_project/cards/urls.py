from django.urls import path

from . import views

app_name = 'cards'

urlpatterns = [
    path('cards/<int:card_id>/edit/', views.card_edit, name='card_edit'),
    path('cards/<int:card_id>/delete/', views.card_delete, name='delete'),
    path('gift/', views.show_gift, name='gift'),
    path('loyalty/', views.show_loyalty, name='loyalty'),
    path('credit/', views.show_credit, name='credit'),
    path('create/', views.create_cards, name='generate'),
    path('search/', views.SearchView.as_view(), name='search'),
    path('', views.IndexView.as_view(), name='index'),
]