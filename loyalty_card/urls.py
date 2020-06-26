from django.urls import path
from .views import *

urlpatterns = [
	path('', CardsList.as_view(), name='cards_list_url'),
	path('search/', CardsList.as_view(), name='search_cards'),
	path('generator/', GenerateCards.as_view(), name='generate_card'),
	path('card/update/', UpdateCard.as_view(), name='change_card'),
	path('card/delete/', DeleteCard.as_view(), name='delete_card'),
]