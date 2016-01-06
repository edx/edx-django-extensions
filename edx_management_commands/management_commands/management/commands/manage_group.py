"""
Management command `manage_group` is used to idempotently create Django groups
and set their permissions by name.
"""

from django.apps import apps
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.utils.translation import gettext as _


class Command(BaseCommand):
    # pylint: disable=missing-docstring

    help = 'Creates the specified group, if it does not exist, and sets its permissions.'

    def add_arguments(self, parser):
        parser.add_argument('group_name')
        parser.add_argument('--remove', dest='is_remove', action='store_true')
        parser.add_argument('-p', '--permissions', nargs='*', default=[])

    def _handle_remove(self, group_name):

        try:
            Group.objects.get(name=group_name).delete()  # pylint: disable=no-member
            self.stderr.write(_('Removed group: "{}"').format(group_name))
        except Group.DoesNotExist:
            self.stderr.write(_('Did not find a group with name "{}" - skipping.').format(group_name))
            return

    @transaction.atomic
    def handle(self, group_name, is_remove, permissions=None, *args, **options):

        if is_remove:
            return self._handle_remove(group_name)

        old_permissions, new_permissions = [], []
        group, created = Group.objects.get_or_create(name=group_name)  # pylint: disable=no-member

        if created:
            try:
                # Needed for sqlite backend (i.e. in tests) because
                # name.max_length won't be enforced by the db.
                # See also http://www.sqlite.org/faq.html#q9
                group.full_clean()
            except ValidationError, exc:
                # give a more helpful error
                raise CommandError(
                    _(
                        'Invalid group name: "{group_name}". {messages}'
                    ).format(
                        group_name=group_name,
                        messages=exc.messages[0]
                    )
                )
            self.stderr.write(_('Created new group: "{}"').format(group_name))
        else:
            self.stderr.write(_('Found existing group: "{}"').format(group_name))
            old_permissions = list(group.permissions.all())

        # resolve the specified permissions
        for permission in permissions or []:

            try:
                app_label, model_name, codename = permission.split(':')
            except ValueError:
                # give a more helpful error
                raise CommandError(_(
                    'Invalid permission option: "{}". Please specify permissions '
                    'using the format: app_label:model_name:permission_codename.'
                ).format(permission))
            # this will raise a LookupError if it fails.
            try:
                model_class = apps.get_model(app_label, model_name)
            except LookupError, exc:
                raise CommandError(exc.message)

            content_type = ContentType.objects.get_for_model(model_class)
            try:
                new_permission = Permission.objects.get(  # pylint: disable=no-member
                    content_type=content_type,
                    codename=codename,
                )
            except Permission.DoesNotExist:
                # give a more helpful error
                raise CommandError(
                    _(
                        'Invalid permission codename: "{codename}".  No such permission exists '
                        'for the model {module}.{model_name}.'
                    ).format(
                        codename=codename,
                        module=model_class.__module__,
                        model_name=model_class.__name__,
                    )
                )
            new_permissions.append(new_permission)

        add_permissions = [p for p in new_permissions if p not in old_permissions]
        remove_permissions = [p for p in old_permissions if p not in new_permissions]

        if add_permissions:
            for ap in add_permissions:
                self.stderr.write(
                    _(
                        'Adding "{codename}" permission to group "{group}"'
                    ).format(
                        codename=ap.codename, group=group_name
                    )
                )
                group.permissions.add(ap)
        else:
            self.stderr.write(_('No permissions to add to group "{}"').format(group_name))

        if remove_permissions:
            for rp in remove_permissions:
                self.stderr.write(
                    _(
                        'Removing "{codename}" permission from group "{group}"'
                    ).format(
                        codename=rp.codename,
                        group=group_name,
                    )
                )
                group.permissions.remove(rp)
        else:
            self.stderr.write(_('No permissions to remove from group "{}"').format(group_name))

        group.save()
