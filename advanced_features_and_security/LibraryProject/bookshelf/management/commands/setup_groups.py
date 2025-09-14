from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from bookshelf.models import Book, Author

class Command(BaseCommand):
    help = 'Setup default user groups with permissions'

    def handle(self, *args, **options):
        # Get content types
        book_content_type = ContentType.objects.get_for_model(Book)
        author_content_type = ContentType.objects.get_for_model(Author)

        # Get all permissions
        book_permissions = Permission.objects.filter(content_type=book_content_type)
        author_permissions = Permission.objects.filter(content_type=author_content_type)

        # Create Viewers group (read-only access)
        viewers_group, created = Group.objects.get_or_create(name='Viewers')
        viewers_group.permissions.set([
            Permission.objects.get(codename='can_view_book'),
            Permission.objects.get(codename='can_view_author'),
        ])
        self.stdout.write(self.style.SUCCESS('Viewers group created/updated'))

        # Create Editors group (create and edit access)
        editors_group, created = Group.objects.get_or_create(name='Editors')
        editors_group.permissions.set([
            Permission.objects.get(codename='can_view_book'),
            Permission.objects.get(codename='can_create_book'),
            Permission.objects.get(codename='can_edit_book'),
            Permission.objects.get(codename='can_view_author'),
            Permission.objects.get(codename='can_create_author'),
            Permission.objects.get(codename='can_edit_author'),
        ])
        self.stdout.write(self.style.SUCCESS('Editors group created/updated'))

        # Create Admins group (full access)
        admins_group, created = Group.objects.get_or_create(name='Admins')
        admins_group.permissions.set(list(book_permissions) + list(author_permissions))
        self.stdout.write(self.style.SUCCESS('Admins group created/updated'))

        self.stdout.write(self.style.SUCCESS('All groups setup successfully!'))
        