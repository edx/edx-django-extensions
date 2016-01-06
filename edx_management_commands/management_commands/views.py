"""
This dummy view is here (along with its associated url conf) to allow Django
checks to pass when developing / testing management commands.

If/when additional Django apps are added to this project which implement
actual views/urls, this dummy view can be disposed of.
"""

from django.http import HttpResponse


def index(__):  # pylint: disable=missing-docstring
    return HttpResponse("This view exists only to placate url checks.")
