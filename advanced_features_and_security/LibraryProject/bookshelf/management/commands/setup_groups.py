

from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.apps import apps

class Command(BaseCommand):
    help = "Creates Viewer, Editor, and Admin groups with Book permissions"

    def handle(self, *args, **options):
        Book = apps.get_model('bookshelf', 'Book')
        perms = Permission.objects.filter(content_type__app_label='bookshelf',
                                          content_type__model='book')

        mapping = {
            'Viewers':  ['can_view'],
            'Editors':  ['can_view', 'can_create', 'can_edit'],
            'Admins':   ['can_view', 'can_create', 'can_edit', 'can_delete'],
        }

        for group_name, codenames in mapping.items():
            group, _ = Group.objects.get_or_create(name=group_name)
            group.permissions.set(perms.filter(codename__in=codenames))
            group.save()
            self.stdout.write(f"Group '{group_name}' configured.")
