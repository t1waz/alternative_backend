from .models import Station


class StationService:
	def get_stations(self):
		return Station.objects.all()

	def get_station(self, station_id):
		try:
			station = Station.objects.get(id=station_id)
		except:
			station = ''

		return station
