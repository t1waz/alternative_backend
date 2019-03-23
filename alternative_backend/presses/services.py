from .models import Press


class PressService:
	def get_presses(self):
		return Press.objects.all()

	def get_press(self, press_id):
		try:
			press = Press.objects.get(id=press_id)
		except:
			press = ''

		return press
