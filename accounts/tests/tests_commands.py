from django.test import TestCase
from django.contrib.auth.models import User, Group
import datetime
from datetime import timedelta
from django.core import mail
from django.core.management import call_command
# Create your tests here.

class CommandTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        
        cls.PASSWORD = 'insecurePassw0rD!'
        
        cls.bazaar_superuser_group = Group.objects.create(name = 'Bazaar Superuser')
        cls.bazaar_superuser_group.save()

        cls.bazaar_moderator_group = Group.objects.create(name = 'Bazaar Moderator')
        cls.bazaar_moderator_group.save()

        cls.superuser = User.objects.create_superuser(username = 'admin', password = cls.PASSWORD)
        cls.superuser.email = 'admin@scullsuite.com'
        cls.superuser.save()

        cls.bazaar_superuser = User.objects.create_user(username = 'bazaaradmin', password = cls.PASSWORD)
        cls.bazaar_superuser.groups.add(cls.bazaar_superuser_group)
        cls.bazaar_superuser.email = 'bazaaradmin@scullsuite.com'
        cls.bazaar_superuser.save()

        cls.bazaar_moderator = User.objects.create_user(username = 'alice', password = cls.PASSWORD)
        cls.bazaar_moderator.groups.add(cls.bazaar_moderator_group)
        cls.bazaar_moderator.email = 'alice@scullsuite.com'
        cls.bazaar_moderator.save()

        cls.inactive_user_0 = User.objects.create_user(username = 'bob', password = cls.PASSWORD)
        cls.inactive_user_0.email = 'bob@scullsuite.com'
        cls.inactive_user_0.last_login = datetime.date.today() - timedelta(366)
        cls.inactive_user_0.save()

        cls.inactive_user_1 = User.objects.create_user(username = 'charlie', password = cls.PASSWORD)
        cls.inactive_user_1.email = 'charlie@scullsuite.com'
        cls.inactive_user_1.last_login = datetime.date.today() - timedelta(366)
        cls.inactive_user_1.save()

        cls.active_user_0 = User.objects.create_user(username = 'duncan', password = cls.PASSWORD)
        cls.active_user_0.email = 'duncan@scullsuite.com'
        cls.active_user_0.save()

        cls.active_user_1 = User.objects.create_user(username = 'eve', password = cls.PASSWORD)
        cls.active_user_1.email = 'eve@scullsuite.com'
        cls.active_user_1.save()

        return super().setUpTestData()

    def test_accounts_notify_inactive_users(self):
        '''
            Test if accounts_notify_inactive_users command send email to users
            that has inactivity for more than 1 month.

            Create users (admin, bazaaradmin, alice, bob, charlie, duncan, eve)
            Two users (charlie, duncan) has more than 30 days of inactivity (modify last_login property).
            Execute bazaar_notify_inactive_users command.
            Check if Django send a email.
            Check if sended email has correct recipients (charlie, duncan)
        '''

        call_command('accounts_notify_inactive_users')

        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].bcc, [self.inactive_user_0.email , self.inactive_user_1.email])

    def test_accounts_delete_inactive_users(self):
        '''
            Test if accounts_delete_inactive_users delete users that has inactivity
            for more than 1 year (365 days)
        '''

        '''
            Create several accounts: 
                admin (superuser)
                bazaaradmin (bazaar superuser)
                alice (bazaar moderator)
                bob (inactive user 0)
                charlie (inactive user 1)
                duncan (active user 0)
                eve (active user 1)

            Execute accounts_delete_inactive_users
            Check if inactive account was deleted (bob and charlie).
        '''

        active_users = User.objects.exclude(last_login__lte = datetime.datetime.today() - timedelta(365))
        
        call_command('accounts_delete_inactive_users')

        self.assertQuerySetEqual(qs = User.objects.all().order_by('id'), values = active_users.order_by('id'))
               