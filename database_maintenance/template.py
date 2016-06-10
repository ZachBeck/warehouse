#!/usr/bin/env python
# * coding: utf8 *
'''
template.py

A module that contains a template for database maintenance pallets
'''

from forklift.models import Pallet
from os.path import join, dirname
from traceback import format_exc

current_folder = dirname(__file__)


class TemplatePallet(Pallet):
    def ship(self):
        try:
            #: code goes here, remove pass
            #: remember to update the paths to database connection files like this:
            #: join(current_folder, 'connection_file.sde')
            pass

        except Exception as e:
            self.send_email('michaelfoulger@utah.gov', 'Error with {}'.format(__file__), format_exc())
            raise e
