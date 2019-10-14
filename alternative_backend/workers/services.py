from workers.models import Worker


class WorkerService:
    def get_worker_from_barcode(self, barcode):
        try:
            return Worker.objects.get(barcode=barcode)
        except (Worker.DoesNotExist, ValueError):
            return None
