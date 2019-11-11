from materials.models import Material


class MaterialService:

	def get_material_from_name(self, material_name):
		return Material.objects.filter(name=material_name).first() or None
