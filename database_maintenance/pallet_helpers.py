#!/usr/bin/env python
# * coding: utf8 *
'''
pallet_helpers.py

A module that contains a base class for all of the pallets in this folder
'''

from forklift.messaging import send_email
from traceback import format_exc
from os.path import splitext


def ship(script_name):
    module_name = splitext(script_name)[0]
    try:
        __import__(module_name)
    except Exception as e:
        send_email('michaelfoulger@utah.gov', 'Error with {}'.format(script_name), format_exc())
        raise e
