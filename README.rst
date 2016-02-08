Part of `edX code`__.

__ http://code.edx.org/

EdX Management Commands  |Travis|_ |Codecov|_
===========================================
.. |Travis| image:: https://travis-ci.org/edx/edx-django-extensions.svg?branch=master
.. _Travis: https://travis-ci.org/edx/edx-django-extensions

.. |Codecov| image:: http://codecov.io/github/edx/edx-django-extensions/coverage.svg?branch=master
.. _Codecov: http://codecov.io/github/edx/edx-django-extensions?branch=master

This repository is intended for Django 1.8 applications and utilities for reuse within
multiple edx-platform projects.

Overview
--------

This package provides a Django application containing management commands that are useful in automated
deployment scenarios.

It currently offers two management commands, ``manage_user`` and ``manage_group``, which are designed to
facilitate idempotent read/write operations on Django users, groups, and permissions.  Consult the source
for more specifics.

Documentation
-------------

The docs for EdX Management Commands are on Read the Docs:  https://edx-management-commands.readthedocs.org.

License
-------

The code in this repository is licensed under LICENSE_TYPE unless
otherwise noted.

Please see ``LICENSE.txt`` for details.

How To Contribute
-----------------

Contributions are very welcome.

Please read `How To Contribute <https://github.com/edx/edx-platform/blob/master/CONTRIBUTING.rst>`_ for details.

Even though they were written with ``edx-platform`` in mind, the guidelines
should be followed for Open edX code in general.

Reporting Security Issues
-------------------------

Please do not report security issues in public. Please email security@edx.org.

Mailing List and Slack Team
---------------------------

You can discuss this code in the `edx-code Google Group`__ or with the `Open edX team on Slack`__.

__ https://groups.google.com/forum/#!forum/edx-code
__ https://openedx-slack-invite.herokuapp.com/
