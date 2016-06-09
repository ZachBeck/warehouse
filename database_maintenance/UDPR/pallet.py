#!/usr/bin/env python
# * coding: utf8 *
'''
pallet.py

A module that contains a pallet to be run in forklift
'''

from forklift.models import Pallet
from os import path
import sys

sys.path.append(path.dirname(path.dirname(__file__)))
import pallet_helpers


class UDPRPallet(Pallet):
    def ship(self):
        pallet_helpers.ship('udpr.py')
