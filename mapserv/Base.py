#!/usr/bin/env python
# * coding: utf8 *
'''
Base.py

A module that contains the pallets for the map services in the base directory of arcgis server
'''

from forklift.models import Pallet
from os.path import join


class LandUsePlanningPallet(Pallet):

    def __init__(self):
        super(LandUsePlanningPallet, self).__init__()

        self.arcgis_services = [('LandUsePlanning', 'MapServer')]

        self.political = 'C:\\Scheduled\\Staging\\Political.gdb'

        self.copy_data = [self.political]
        self.destination_coordinate_system = 26912

    def build(self, configuration=None):
        source_workspace = join(self.garage, 'SGID10.sde')

        self.add_crates(
            ['UtahHouseDistricts2012', 'UtahSenateDistricts2012', 'DistrictCombinationAreas2012'],
            {'source_workspace': source_workspace,
             'destination_workspace': self.political})


class PoliticalDistrictsPallet(Pallet):

    def __init__(self):
        super(PoliticalDistrictsPallet, self).__init__()

        self.arcgis_services = [('PoliticalDistricts', 'MapServer')]

        self.political = 'C:\\Scheduled\\Staging\\Political.gdb'

        self.copy_data = [self.political]
        self.destination_coordinate_system = 26912

    def build(self, configuration=None):
        source_workspace = join(self.garage, 'SGID10.sde')

        self.add_crates(
            ['UtahHouseDistricts2012', 'UtahSenateDistricts2012', 'DistrictCombinationAreas2012'],
            {'source_workspace': source_workspace,
             'destination_workspace': self.political})


class SocrataPallet(Pallet):

    def __init__(self):
        super(SocrataPallet, self).__init__()

        self.arcgis_services = [('Socrata', 'MapServer')]

        self.political = 'C:\\Scheduled\\Staging\\Political.gdb'
        self.boundaries = 'C:\\Scheduled\\Staging\\Boundaries.gdb'
        self.society = 'C:\\Scheduled\\Staging\\Society.gdb'
        self.energy = 'C:\\Scheduled\\Staging\\Energy.gdb'
        self.economy = 'C:\\Scheduled\\Staging\\Economy.gdb'

        self.copy_data = [self.political, self.boundaries, self.society, self.energy, self.economy]

    def build(self, configuration=None):
        source_workspace = join(self.garage, 'SGID10.sde')

        self.add_crates(['Municipalities', 'SchoolDistricts'], {'source_workspace': source_workspace,
                                                                'destination_workspace': self.boundaries})

        self.add_crates(
            ['UtahHouseDistricts2012', 'UtahSenateDistricts2012', 'UtahSchoolBoardDistricts2012'],
            {'source_workspace': source_workspace,
             'destination_workspace': self.political})

        self.add_crates(['Schools'], {'source_workspace': source_workspace, 'destination_workspace': self.society})

        self.add_crates(['DNROilGasWells'], {'source_workspace': source_workspace,
                                             'destination_workspace': self.energy})

        self.add_crates(['TaxEntities2014'], {'source_workspace': source_workspace,
                                              'destination_workspace': self.economy})
