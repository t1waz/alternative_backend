from .models import Station


class StationService:
	def get_stations(self):
		return Station.objects.all()

	def get_station(self, station_id):
		return Station.objects.get(id=station_id)