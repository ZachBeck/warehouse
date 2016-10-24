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

        self.arcgis_services = [('BaseMaps/AddressPoints', 'MapServer'), ('BaseMaps/Hillshade', 'MapServer')]

        staging = 'C:\\Scheduled\\staging'
        self.transportation = join(staging, 'transportation_utm.gdb')
        self.boundaries = join('boundaries_utm.gdb')
        self.location = join('location_utm.gdb')

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
