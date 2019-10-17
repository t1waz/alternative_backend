from workers.models import Worker


class WorkerService:
    def get_worker_from_barcode(self, barcode):
        try:
            return Worker.objects.get(barcode=barcode)
        except (Worker.DoesNotExist, ValueError):
            return None

    def get_passwords(self):
    	return [password for password in 
    			Worker.objects.all().values_list('password', flat=True)]
