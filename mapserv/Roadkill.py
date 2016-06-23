#!/usr/bin/env python
# * coding: utf8 *
'''
Roadkill.py

A module that contains the pallets for the roadkill folder in mapserv.
'''

from forklift.models import Pallet
from os.path import join


class RoadKillPallet(Pallet):

    def __init__(self):
        super(RoadKillPallet, self).__init__()

        self.arcgis_services = [('RoadKill/Overlays', 'MapServer'), ('RoadKill/Toolbox', 'GPServer')]

        self.transportation = 'C:\\Scheduled\\Staging\\Transportation.gdb'

        self.copy_data = [self.transportation]
        self.destination_coordinate_system = 26912

    def build(self, configuration=None):
        source_workspace = join(self.garage, 'SGID10.sde')

        self.add_crates(['UDOTMileposts', 'UDOTRoutes_LRS'], {'source_workspace': source_workspace,
                                                              'destination_workspace': self.transportation})
