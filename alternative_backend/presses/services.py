from django.dispatch import receiver
from boards.models import BoardModel
from django.db.models.signals import pre_save
from .models import Press


@receiver(pre_save, sender=Press)
def handle_history(sender, instance, **kwargs):
    current_press = Press.objects.get(id=instance.id)
    last_mold = BoardModel.objects.get(id=current_press.tracker.previous('mold')).name
    current_mold = instance.mold.name
    if last_mold != current_mold:
        pass
        # DO HISTORY SHIT
