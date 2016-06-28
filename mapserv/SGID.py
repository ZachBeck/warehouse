#!/usr/bin/env python
# * coding: utf8 *
'''
SGID.py

A module that contains the pallets for the SGID folder in mapserve.
'''

from forklift.models import Pallet
from os.path import join


class SgidPallet(Pallet):

    def __init__(self):
        super(SgidPallet, self).__init__()

        self.arcgis_services = [('SGID/CountyBoundaries', 'MapServer'), ('SGID/DOGM', 'MapServer'),
                                ('SGID/LandOwnership', 'MapServer')]

        self.energy = 'C:\\Scheduled\\Staging\\Energy_UTM.gdb'
        self.boundaries = 'C:\\Scheduled\\Staging\\Boundaries_UTM.gdb'
        self.cadastre = 'C:\\Scheduled\\Staging\\Cadastre_UTM.gdb'

        self.copy_data = [self.energy, self.boundaries, self.cadastre]
        self.destination_coordinate_system = 26912

    def build(self, configuration=None):
        source_workspace = join(self.garage, 'SGID10.sde')

        self.add_crates(['Counties'], {'source_workspace': source_workspace, 'destination_workspace': self.boundaries})

        self.add_crates(['DNROilGasWells_HDPath'], {'source_workspace': source_workspace,
                                                    'destination_workspace': self.energy})

        self.add_crates(['LandOwnership'], {'source_workspace': source_workspace,
                                            'destination_workspace': self.cadastre})
