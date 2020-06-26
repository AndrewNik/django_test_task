from django import forms
from dateutil.relativedelta import relativedelta


class GenCards(forms.Form):
	date_deltas = {
		'1 месяц': relativedelta(months=1),
		'6 месяцев': relativedelta(months=6),
		'1 год': relativedelta(years=1)
	}

	date_term = forms.ChoiceField(choices=[(key, key) for key in date_deltas], label='Срок действия: ')
	date_term.widget.attrs.update({'class': 'form-control'})

	series = forms.IntegerField(label='Серия карт: ', min_value=0)
	series.widget.attrs.update({'class': 'form-control', 'placeholder': 'Серия'})

	count = forms.IntegerField(label='Количество карт: ', min_value=0)
	count.widget.attrs.update({'class': 'form-control', 'placeholder': 'Кол-во карт'})


class SearchCards(forms.Form):
	search_params = [
		('series', 'серия'),
		('number', 'номер'),
		('release_date', 'дата выпуска'),
		('end_date', 'дата окончания'),
		('status', 'статус')
	]

	search = forms.ChoiceField(choices=search_params, label='Параметры поиска: ', required=False)
	search.widget.attrs.update({'class': 'form-control'})

	search_reg = forms.CharField(required=False)
	search_reg.widget.attrs.update({'class': 'form-control', 'placeholder': 'Строка запроса'})
