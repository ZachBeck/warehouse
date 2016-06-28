#!/usr/bin/env python
# * coding: utf8 *
'''
LtGovPoliticalDistricts.py

A module that contains a pallet to update the services in LtGovPoliticalDistricts on mapserv
'''

from forklift.models import Pallet
from os.path import join


class LtGovPoliticalDistrictsPallet(Pallet):

    def __init__(self):
        super(LtGovPoliticalDistrictsPallet, self).__init__()

        self.arcgis_services = [('LtGovPoliticalDistricts/Districts', 'MapServer'),
                                ('LtGovPoliticalDistricts/Labels', 'MapServer')]

        self.political = 'C:\\Scheduled\\Staging\\Political.gdb'

        self.copy_data = [self.political]

    def build(self, configuration=None):
        source_workspace = join(self.garage, 'SGID10.sde')

        self.add_crates(
            ['USCongressDistricts2012', 'UtahSenateDistricts2012', 'UtahHouseDistricts2012',
             'UtahSchoolBoardDistricts2012'], {'source_workspace': source_workspace,
                                               'destination_workspace': self.political})
