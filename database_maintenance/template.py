#!/usr/bin/env python
# * coding: utf8 *
'''
template.py

A module that contains a template for database maintenance pallets
'''

from forklift.models import Pallet
from os.path import join
from traceback import format_exc
import arcpy


class TemplatePallet(Pallet):
    def ship(self):
        try:
            #: code goes here
            #: replace print statements with self.log.info
            #: remember to update the paths to database connection files like this:
            #: join(self.garage, 'FOLDERS?', 'connection_file.sde')

        except Exception as e:
            self.send_email('michaelfoulger@utah.gov', 'Error with {}'.format(__file__), format_exc())
            raise e
