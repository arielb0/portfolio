from django.core.management import BaseCommand, CommandError
from django.contrib.auth.models import User
from datetime import datetime, timedelta
from django.core.mail import EmailMessage
from django.db.models import Q

class Command(BaseCommand):
    help = 'Notify inactive users'

    def handle(self, *args, **options):
        '''
            Get inactive users (users with 30 days or more of inactivity).
            Exclude from the user list bazaaradmin and admin user.
            Send email saying that Bazaar missing them.
        '''       
        # TODO: This command is better placed on accounts application.
        # TODO: You can include the most popular ads on mail.
        # TODO: You can include a recommended ads for user (more dificult).
        # All members of the recipient list will see other recipient address on To field. These
        # is wrong, because an attacker could obtain a list of users and make spam.

        users = User.objects.filter(last_login__lte = datetime.now() - timedelta(days = 30))
        users = users.exclude(Q(is_superuser = True) | Q(groups__name = 'Bazaar Superuser') | Q(groups__name = 'Bazaar Moderator')) # Exlude bazaar superuser and moderators. Use is_superuser property and bazaar_moderator group.
        recipient_list = users.values_list('email', flat=True)

        if len(recipient_list) > 0:
        
            email = EmailMessage(
                subject = 'Scull Suite missing you!',
                body = '''
                        I seems that you do not login on Scull Suite on long time. It is a shame.
                        We have new content that could interest you!

                        Remember, if your account is inactive for a year, it will deleted automatically,
                        to avoid bother you and optimize our systems.
                    ''',
                bcc = recipient_list
                )
            email_send_successfully = email.send()
            if email_send_successfully == 1:
                print(f'Notified {users.count()} inactive users.')
            else:
                raise CommandError('Message could not be send.')
            
        else:
            print('Could not have inactive users to notify for inactivity.')

        