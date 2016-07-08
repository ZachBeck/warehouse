#!/usr/bin/env python
# * coding: utf8 *
'''
SurfaceWaterQuality.py

A module that contains a pallet to update the services in SurfaceWaterQuality on mapserv
'''

from forklift.models import Pallet
from os.path import join


class SurfaceWaterQualityPallet(Pallet):

    def __init__(self):
        super(SurfaceWaterQualityPallet, self).__init__()

        self.arcgis_services = [('SurfaceWaterQuality/MapService', 'MapServer'),
                                ('SurfaceWaterQuality/Toolbox', 'GPServer')]

        self.water = 'C:\\Scheduled\\Staging\\water.gdb'

        self.copy_data = [self.water]

    def build(self, configuration=None):
        source_workspace = join(self.garage, 'SGID10.sde')

        self.add_crates(['StreamsNHDHighRes'], {'source_workspace': source_workspace,
                                                'destination_workspace': self.water})
