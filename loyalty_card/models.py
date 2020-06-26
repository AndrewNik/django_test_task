from django.db import models
from django.shortcuts import reverse

# Create your models here.


class Cards(models.Model):
	class Status(models.TextChoices):
		INACTIVE = "не активирована"
		ACTIVE = "активирована"
		EXPIRED = "просрочена"

	class Meta:
		unique_together = (('series', 'number'),)

	series = models.PositiveIntegerField(db_index=True)
	number = models.PositiveIntegerField(db_index=True)
	release_date = models.DateTimeField(auto_now_add=True)
	end_date = models.DateTimeField()
	use_date = models.DateTimeField(blank=True, null=True)
	amount = models.FloatField(null=True, blank=True, default=0)
	status = models.CharField(choices=Status.choices, default=Status.INACTIVE, max_length=150)

	def __str__(self):
		return f'{self.series, self.number}'

