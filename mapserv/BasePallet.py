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

        self.bioscience = 'C:\\Scheduled\\Staging\\bioscience_utm.gdb'
        self.boundaries = 'C:\\Scheduled\\Staging\\boundaries_utm.gdb'
        self.cadastre = 'C:\\Scheduled\\Staging\\cadastre_utm.gdb'
        self.geoscience = 'C:\\Scheduled\\Staging\\geoscience_utm.gdb'
        self.health = 'C:\\Scheduled\\Staging\\health_utm.gdb'
        self.history = 'C:\\Scheduled\\Staging\\history_utm.gdb'
        self.location = 'C:\\Scheduled\\Staging\\location_utm.gdb'
        self.planning = 'C:\\Scheduled\\Staging\\planning_utm.gdb'
        self.society = 'C:\\Scheduled\\Staging\\society_utm.gdb'
        self.transportation = 'C:\\Scheduled\\Staging\\transportation_utm.gdb'
        self.water = 'C:\\Scheduled\\Staging\\water_utm.gdb'

        self.copy_data = [self.bioscience, self.boundaries, self.cadastre, self.geoscience, self.health, self.history,
                          self.location, self.planning, self.society, self.transportation, self.water]
        self.destination_coordinate_system = 26912

    def build(self, configuration=None):
        source_workspace = join(self.garage, 'SGID10.sde')

        self.add_crates(
            ['Habitat_RingNeckedPheasant', 'Habitat_Pronghorn', 'Habitat_Muledeer', 'Habitat_RockyMountainElk',
             'DominantVegetation'], {'source_workspace': source_workspace,
                                     'destination_workspace': self.bioscience})

        self.add_crates(['Municipalities', 'SchoolDistricts'], {'source_workspace': source_workspace,
                                                                'destination_workspace': self.boundaries})

        self.add_crates(
            ['Parcels_Wasatch', 'Parcels_Wayne', 'Parcels_Uintah', 'Parcels_Utah', 'Parcels_Daggett', 'Parcels_Iron',
             'Parcels_Juab', 'Parcels_Beaver', 'LandOwnership', 'Parcels_Summit', 'Parcels_Cache', 'Parcels_Sanpete',
             'Parcels_Washington', 'Parcels_Weber', 'Parcels_Grand', 'Parcels_Millard', 'Parcels_Emery',
             'PLSSTownships_GCDB', 'PLSSSections_GCDB', 'Parcels_Carbon', 'Parcels_SanJuan', 'Parcels_BoxElder',
             'Parcels_Davis', 'Parcels_SaltLake', 'Parcels_Tooele', 'Parcels_Rich'],
            {'source_workspace': source_workspace,
             'destination_workspace': self.cadastre})

        self.add_crates(['Soils', 'QuaternaryFaults', 'AvalanchePaths', 'LiquefactionPotential'],
                        {'source_workspace': source_workspace,
                         'destination_workspace': self.geoscience})

        self.add_crates(['HealthCareFacilities'], {'source_workspace': source_workspace,
                                                   'destination_workspace': self.health})

        self.add_crates(['HistoricDistricts'], {'source_workspace': source_workspace,
                                                'destination_workspace': self.history})

        self.add_crates(['PlaceNamesGNIS2000'], {'source_workspace': source_workspace,
                                                 'destination_workspace': self.location})

        self.add_crates(['WildernessProp_WDesert1999', 'ConservationEasements', 'WaterRelatedLandUse'],
                        {'source_workspace': source_workspace,
                         'destination_workspace': self.planning})

        self.add_crates(['Cemeteries', 'Schools', 'Libraries'], {'source_workspace': source_workspace,
                                                                 'destination_workspace': self.society})

        self.add_crates(['Railroads', 'Airports', 'Roads'], {'source_workspace': source_workspace,
                                                             'destination_workspace': self.transportation})
        self.add_crates(
            ['Wetlands', 'SpringsNHDHighRes', 'Streams', 'SummitCoFloodZones', 'Floodplains', 'Watersheds_Area',
             'ParagonahFloodZones', 'LakesNHDHighRes', 'WeberCoFloodZones'], {'source_workspace': source_workspace,
                                                                              'destination_workspace': self.water})


class PoliticalDistrictsPallet(Pallet):

    def __init__(self):
        super(PoliticalDistrictsPallet, self).__init__()

        self.arcgis_services = [('PoliticalDistricts', 'MapServer')]

        self.political = 'C:\\Scheduled\\Staging\\political_utm.gdb'

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

        self.political = 'C:\\Scheduled\\Staging\\political.gdb'
        self.boundaries = 'C:\\Scheduled\\Staging\\boundaries.gdb'
        self.society = 'C:\\Scheduled\\Staging\\society.gdb'
        self.energy = 'C:\\Scheduled\\Staging\\energy.gdb'
        self.economy = 'C:\\Scheduled\\Staging\\economy.gdb'

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
