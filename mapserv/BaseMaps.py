#!/usr/bin/env python
# * coding: utf8 *
'''
BaseMaps.py

A module that contains a pallet to update the querable layers behind our UTM basemaps
'''

from forklift.models import Pallet
from os.path import join


class BaseMapsPallet(Pallet):

    def __init__(self):
        super(BaseMapsPallet, self).__init__()

        self.arcgis_services = [('BaseMaps/AddressPoints', 'MapServer'), ('BaseMaps/Hillshade', 'MapServer'),
                                ('BaseMaps/Hybrid', 'MapServer'), ('BaseMaps/Lite', 'MapServer'),
                                ('BaseMaps/Terrain', 'MapServer'), ('BaseMaps/Topo', 'MapServer'),
                                ('BaseMaps/Vector', 'MapServer')]

        self.transportation = 'C:\\Scheduled\\Staging\\Transportation.gdb'
        self.boundaries = 'C:\\Scheduled\\Staging\\Boundaries.gdb'
        self.location = 'C:\\Scheduled\\Staging\\Location.gdb'

        self.copy_data = [self.transportation, self.boundaries, self.location]
        self.destination_coordinate_system = 26912

    def build(self, configuration=None):
        source_workspace = join(self.garage, 'SGID10.sde')

        self.add_crates(['Roads'], {'source_workspace': source_workspace, 'destination_workspace': self.transportation})

        self.add_crates(['Municipalities_Carto', 'Counties'], {'source_workspace': source_workspace,
                                                               'destination_workspace': self.boundaries})

        self.add_crates(['ZoomLocations', 'PlaceNamesGNIS2000', 'AddressPoints'],
                        {'source_workspace': source_workspace,
                         'destination_workspace': self.location})
