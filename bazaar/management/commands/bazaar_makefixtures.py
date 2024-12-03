from typing import Any
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import Permission, Group
from django.db.models import Q
from django.core.serializers import serialize
from scull_suite.settings import BASE_DIR


class Command(BaseCommand):
    requires_migrations_checks = True
    help = 'Generate fixtures that contain default permission and groups.'

    def handle(self, *args: Any, **options: Any) -> str | None:
        try:            

            moderator_permissions = [
                Permission.objects.get(codename = 'moderate_ad'),
                Permission.objects.get(codename = 'view_report'),
            ]

            superuser_permissions = moderator_permissions.copy()

            superuser_permissions.extend([
                Permission.objects.get(codename = 'add_currency'),
                Permission.objects.get(codename = 'view_currency'),
                Permission.objects.get(codename = 'change_currency'),
                Permission.objects.get(codename = 'delete_currency'),
                Permission.objects.get(codename = 'add_category'),
                Permission.objects.get(codename = 'view_category'),
                Permission.objects.get(codename = 'change_category'),
                Permission.objects.get(codename = 'delete_category'),
                Permission.objects.get(codename = 'change_ad'),
                Permission.objects.get(codename = 'delete_ad'),
                Permission.objects.get(codename = 'add_report'),
                Permission.objects.get(codename = 'change_report'),
                Permission.objects.get(codename = 'delete_report'),
                Permission.objects.get(codename = 'add_user'),
                Permission.objects.get(codename = 'view_user'),
                Permission.objects.get(codename = 'change_user'),
                Permission.objects.get(codename = 'delete_user')]
            )

            moderator_group_name = 'Bazaar Moderator'
            superuser_group_name = 'Bazaar Superuser'
            
            moderator_group = Group.objects.get_or_create(name = moderator_group_name)[0]
            superuser_group = Group.objects.get_or_create(name = superuser_group_name)[0]

            moderator_group.permissions.set(moderator_permissions)
            superuser_group.permissions.set(superuser_permissions)
            moderator_group.save()
            superuser_group.save()

            permission_query = Q()
            for model in ['currency', 'category', 'ad', 'report']:
                permission_query = Q(
                    permission_query | 
                    Q(codename = f'add_{model}') |
                    Q(codename = f'view_{model}') |
                    Q(codename = f'change_{model}') |
                    Q(codename = f'delete_{model}')
                )

            serialized_permissions = serialize('json', Permission.objects.filter(permission_query))

            serialized_groups = serialize('json', Group.objects.filter(Q(name = moderator_group_name) | Q(name = superuser_group_name)))

            bazaar_fixtures_path = '/bazaar/fixtures/bazaar/'

            with open(f'{BASE_DIR}{bazaar_fixtures_path}permissions.json', 'w') as permissions_fixture:
                permissions_fixture.write(serialized_permissions)

            with open(f'{BASE_DIR}{bazaar_fixtures_path}groups.json', 'w') as groups_fixtures:
                groups_fixtures.write(serialized_groups)

            print('Fixtures are generated successfully.')
            
        except:
            raise CommandError("Fixtures can not generated. Please, check if all your migrations are applied to database.")