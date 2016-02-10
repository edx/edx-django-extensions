Management Commands
===================


Use Case
--------
These management commands are designed for use when there is a need to programmatically create
or update Django users, groups, and permissions, without needing to hardcode these in migrations or
application code.

The commands are designed to work idempotently - that is, running them multiple times
with the same inputs should always result in the same outcomes, and without additional side-effects if they
are run more than once.


manage_group
------------
The ``manage_group`` command is used to ensure that a specific :py:class:`django.contrib.auth.models.Group` exists, and that it has a specific set of
permissions.

The following example will create a group named ``mygroup`` if it does not exist (and will do nothing if it does exist):

.. code-block:: bash

    $ python manage.py manage_group mygroup


The following example will create or update the group named ``privileged_group`` and assign to it the permissions
for adding and deleting instances of model "Thing" in "myapp":

.. code-block:: bash

    $ python manage.py manage_group privileged_group -p myapp:Thing:add_thing myapp:Thing:delete_thing

In the above example, if the group already possessed another permission such as "update_thing", that permission would
be automatically removed.


An option to remove, instead of create, is also available:

.. code-block:: bash

    $ python manage.py manage_group mygroup --remove

In the above example, the matching group would be deleted if it existed, and the command would do nothing otherwise.


manage_user
-----------
The ``manage_user`` command is used to ensure that a specific user exists, and that it has a specific set of groups.
It can also be used to toggle the ``is_staff`` and ``is_superuser`` bits on that user account.

The following example will create a user named ``groucho`` if it does not exist:

.. code-block:: bash

    $ python manage.py manage_user groucho groucho@example.com

In the above example, if ``groucho`` already exists, the command will continue without action / error, as long as the
supplied email address matches the one already stored.  If this is not the case, the command will fail with an error.
This is intended as a control measure against potential scripting errors that might cause an existing user to lose
control of an existing account.

To set the staff or superuser bits, use the associated options:

.. code-block:: bash

    $ python manage.py manage_user groucho groucho@example.com --staff --superuser

In the above example, both bits will be set to true.  In order to set the bits to false, omit the options.

To assign a user to specific groups, use the `-g` option:

.. code-block:: bash

    $ python manage.py manage_user groucho groucho@example.com -g mygroup privileged_group

The above will ensure that ``groucho`` will be assigned to ``mygroup`` and ``privileged_group``, and removed from any
others to which they may already have been assigned.

Note that if any of the groups specified with ``-g`` do not exist, the command will output a warning, but will
continue without creating the group. This measure is intended to ensure that, in an automated deployment setting,
a prior misconfiguration involving some particular group will not cause a cascading failure in setting (or removing)
other group memberships.

An option to remove, instead of create, is also available:

.. code-block:: bash

    $ python manage.py manage_user groucho groucho@example.com --remove

In the above example, the matching user would be deleted if it existed, and the command would do nothing otherwise.
