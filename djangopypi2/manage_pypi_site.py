#!/usr/bin/env python
#######################
from __future__ import unicode_literals, print_function
#######################
import os
import sys

def main():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "djangopypi2.website.settings")
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)
    
if __name__ == "__main__":
    main()
