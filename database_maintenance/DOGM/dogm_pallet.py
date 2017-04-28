#!/usr/bin/env python
# * coding: utf8 *
'''
dogm_pallet.py

A module that contains a pallet that updates data in the DOGM database from SGID
'''


from forklift.models import Pallet
from os.path import join


class DOGMPallet(Pallet):
    def build(self, configuration=None):
        sgid = join(self.garage, 'SGID10.sde')
        dogm_admin = join(self.garage, 'dogm', 'DOGMADMIN@DOGM@dogm.agrc.utah.gov.sde')
        dogm_wells = join(self.garage, 'dogm', 'OilGas@DOGM@dogm.agrc.utah.gov.sde')

        self.add_crates(['LandOwnership', 'PLSSQuarterQuarterSections_GCDB'], {
            'source_workspace': sgid,
            'destination_workspace': dogm_admin
        })
        self.add_crate(('DNROilGasWells', sgid, dogm_wells, 'OilGasWells_sde'))
