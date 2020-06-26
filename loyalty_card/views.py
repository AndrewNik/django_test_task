from django.shortcuts import render
from django.http import JsonResponse, QueryDict
from django.views import View
from datetime import datetime
from .models import *
from .forms import *
from django.utils.timezone import make_aware

# Create your views here.

class CardsList(View):
	def get(self, request):
		self.check_status()
		search_form = SearchCards()
		c_list = Cards.objects.all()
		return render(request, 'loyalty_card/index.html', context={'page_obj': c_list, 'search': search_form})

	def post(self, request):
		self.check_status()
		bound_form = SearchCards(request.POST)
		c_list = Cards.objects.all()
		if bound_form.is_valid():
			data = bound_form.cleaned_data
			try:
				if data['search_reg']:
					c_list = Cards.objects.filter(**{data['search']: data['search_reg']})
			except Exception as ex:
				bound_form.add_error('search_reg', ex.__str__())
		return render(request, 'loyalty_card/index.html', context={'page_obj': c_list, 'search': bound_form})

	def check_status(self):
		for card in Cards.objects.all():
			if card.end_date <= make_aware(datetime.now()):
				card.status = Cards.Status.EXPIRED
				card.save()



class UpdateCard(View):

	def post(self, request):
		card_data = request.POST.dict()
		try:
			card = Cards.objects.get(series__exact=card_data['series'], number__exact=card_data['number'])
			card.status = card_data['status']
			card.save()
			return JsonResponse({'result': True})
		except:
			return JsonResponse({'result': False})


class DeleteCard(View):

	def delete(self, request):
		card_data = QueryDict(request.body).dict()
		try:
			card = Cards.objects.get(series__exact=card_data['series'], number__exact=card_data['number'])
			card.delete()
			return JsonResponse({'result': True})
		except:
			return JsonResponse({'result': False})


class GenerateCards(View):

	def get(self, request):
		return render(request, 'loyalty_card/generator.html', context={'form': GenCards()})

	def post(self, request):
		bound_form = GenCards(request.POST)

		if bound_form.is_valid():
			data = bound_form.cleaned_data
			max_num_card = Cards.objects.filter(series=data['series']).order_by('-number')
			start_idx = max_num_card.number + 1 if max_num_card else 0
			for i in range(start_idx, start_idx + data['count']):
				Cards.objects.create(
					series=data['series'],
					number=i,
					end_date=make_aware(datetime.now() + GenCards.date_deltas[data['date_term']])
				)

			return render(request, 'loyalty_card/generator.html', context={'form': GenCards()})

		return render(request, 'loyalty_card/generator.html', context={'form': bound_form})
