from django.core.management import BaseCommand, CommandError
from django.contrib.auth.models import User
from datetime import datetime, timedelta
from django.core.mail import EmailMessage
from django.db.models import Q

class Command(BaseCommand):
    help = 'Delete inactive users'

    def handle(self, *args, **options):
        '''
            Get inactive users (users with 365 days or more of inactivity).
            Exclude from the user list, users that belong to  Bazaar Superuser and Bazaar Moderator groups
            Delete users on user list.
        '''

        users = User.objects.filter(last_login__lte = datetime.now() - timedelta(days = 30))
        users = users.exclude(Q(is_superuser = True) | Q(groups__name = 'Bazaar Superuser') | Q(groups__name = 'Bazaar Moderator')) # Exlude admins and bazaar moderators. Use is_superuser property and bazaar_moderator group.
        
        if users.count() > 0:
            number_of_deleted_accounts = users.count()
            users.delete()
            print(f'Deleted {number_of_deleted_accounts} inactive accounts.')
        else:
            print('There are not inactive accounts to delete')

        