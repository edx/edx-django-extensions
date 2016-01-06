"""
Management command `manage_user` is used to idempotently create or remove
Django users, set/unset permission bits, and associate groups by name.
"""

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.utils.translation import gettext as _


@transaction.atomic
class Command(BaseCommand):
    # pylint: disable=missing-docstring

    help = 'Creates the specified user, if it does not exist, and sets its groups.'

    def add_arguments(self, parser):
        parser.add_argument('username')
        parser.add_argument('email')
        parser.add_argument('--remove', dest='is_remove', action='store_true')
        parser.add_argument('--superuser', dest='is_superuser', action='store_true')
        parser.add_argument('--staff', dest='is_staff', action='store_true')
        parser.add_argument('-g', '--groups', nargs='*', default=[])

    def _maybe_update(self, user, attribute, new_value):
        """
        DRY helper.  If the specified attribute of the user differs from the
        specified value, it will be updated.
        """
        old_value = getattr(user, attribute)
        if new_value != old_value:
            self.stderr.write(
                _('Setting {attribute} for user "{username}" to "{new_value}"').format(
                    attribute=attribute, username=user.username, new_value=new_value
                )
            )
            setattr(user, attribute, new_value)

    def _check_email_match(self, user, email):
        """
        DRY helper.

        Requiring the user to specify both username and email will help catch
        certain issues, for example if the expected username has already been
        taken by someone else.
        """
        if user.email != email:
            # The passed email address doesn't match this username's email address.
            # Assume a problem and fail.
            raise CommandError(
                _(
                    'Skipping user "{}" because the specified and existing email '
                    'addresses do not match.'
                ).format(user.username)
            )

    def _handle_remove(self, username, email):

        users = get_user_model().objects.filter(username=username)
        if not users:
            self.stderr.write(_('Did not find a user with username "{}" - skipping.').format(username))
            return

        user = users[0]
        self._check_email_match(user, email)
        self.stderr.write(_('Removing user: "{}"').format(user))
        user.delete()

    def handle(self, username, email, is_remove, is_staff, is_superuser, groups, *args, **options):

        if is_remove:
            return self._handle_remove(username, email)

        old_groups, new_groups = [], []
        user, created = get_user_model().objects.get_or_create(username=username)

        if created:
            user.set_unusable_password()
            self.stderr.write(_('Created new user: "{}"').format(user))
            self._maybe_update(user, 'email', email)
        else:
            # NOTE, we will not update the email address of an existing user.
            self.stderr.write(_('Found existing user: "{}"').format(user))
            self._check_email_match(user, email)
            old_groups = list(user.groups.all())

        self._maybe_update(user, 'is_staff', is_staff)
        self._maybe_update(user, 'is_superuser', is_superuser)

        # resolve the specified groups
        for group_name in groups or []:

            try:
                group = Group.objects.get(name=group_name)  # pylint: disable=no-member
                new_groups.append(group)
            except Group.DoesNotExist:
                # warn, but move on.
                self.stderr.write(_('Could not find a group named "{}" - skipping.').format(group_name))

        add_groups = [p for p in new_groups if p not in old_groups]
        remove_groups = [p for p in old_groups if p not in new_groups]

        if add_groups:
            for ag in add_groups:
                self.stderr.write(
                    _(
                        'Adding user "{username}" to group "{group_name}"'
                    ).format(
                        username=username, group_name=ag.name
                    )
                )
                user.groups.add(ag)
        else:
            self.stderr.write(_('Not adding user "{}" to any groups').format(username))

        if remove_groups:
            for rg in remove_groups:
                self.stderr.write(
                    _(
                        'Removing user "{username}" from group "{group_name}"'
                    ).format(
                        username=username, group_name=rg.name
                    )
                )
                user.groups.remove(rg)
        else:
            self.stderr.write(_('Not removing user "{}" from any groups').format(username))

        user.save()
