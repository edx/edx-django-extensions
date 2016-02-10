#!/usr/bin/env python

"""
Django administration utility.
"""

import os
import sys

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "edx_management_commands.settings")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)