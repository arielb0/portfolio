from typing import Any
from django.core.management.base import BaseCommand, CommandError
from bazaar.models import Ad
import datetime
from datetime import timedelta

class Command(BaseCommand):
    help = 'Delete ads older than one month.'

    def handle(self, *args: Any, **options: Any) -> str | None:
        
        actual_date = datetime.datetime.now()
        old_ads = Ad.objects.filter(date__lte = actual_date - timedelta(days = 30))
        objects_deleted = old_ads.delete()
        
        if objects_deleted[0] == 0:
            return 'No old ads to delete!'

        return f'Deleted old ads sucessfully.'