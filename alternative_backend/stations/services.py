from .models import Station


class StationService:
	def get_stations(self):
		return Station.objects.all()