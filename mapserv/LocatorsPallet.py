#!/usr/bin/env python
# * coding: utf8 *
'''
LocatorsPallet.py

A module that contains a pallet definition for data to support the mapserv locator services

Requires:
secrets.py, server.ags and sddrafts/ to be in the same folder.

Tip:
To create the .sddraft files use arcpy.CreateGeocodeSDDraft
'''

import arcpy
from forklift.models import Crate
from forklift.models import Pallet
from os import environ
from os import path

import sys
sys.path.append(path.join(path.realpath(path.dirname(__file__)), 'agrc'))
from agrc import ags


class LocatorsPallet(Pallet):

    def build(self, config):
        self.sgid = path.join(self.garage, 'SGID10.sde')
        self.locators = path.join(self.staging_rack, 'locators.gdb')

        self.add_crates(['AddressPoints', 'Roads'], {'source_workspace': self.sgid, 'destination_workspace': self.locators})

    def post_copy_process(self):
        locators_roads = ['Roads_AddressSystem_ACSALIAS', 'Roads_AddressSystem_ALIAS1', 'Roads_AddressSystem_ALIAS2', 'Roads_AddressSystem_STREET']
        locator_addressPoints = 'AddressPoints_AddressSystem'

        self.agsAdmin = ags.AGSAdmin(environ.get('FORKLIFT_AGS_USERNAME'), environ.get('FORKLIFT_AGS_PASSWORD'), environ.get('FORKLIFT_AGS_SERVER_HOST'))

        if self.get_crates()[0].result[0] in [Crate.CREATED, Crate.UPDATED]:
            self.rebuild_locator(locator_addressPoints)

        if self.get_crates()[1].result[0] in [Crate.CREATED, Crate.UPDATED]:
            for locator in locators_roads:
                self.rebuild_locator(locator)

    def rebuild_locator(self, locator):
        sddraftsFolder = path.join(path.dirname(__file__), 'sddrafts')

        self.log.info('rebuilding {}'.format(locator))
        arcpy.RebuildAddressLocator_geocoding(path.join(self.locators, locator))
        sdFile = '{}\\{}.sd'.format(sddraftsFolder, locator)

        #: clear out any old .sd files
        if arcpy.Exists(sdFile):
            arcpy.Delete_management(sdFile)
        sddraftFile = '{}\\{}.sddraft'.format(sddraftsFolder, locator)
        if arcpy.Exists(sddraftFile):
            arcpy.Delete_management(sddraftFile)

        #: delete existing locator service
        service = 'Geolocators/' + locator
        serviceType = 'GeocodeServer'
        self.log.info('deleting existing service')
        try:
            self.agsAdmin.deleteService(service, serviceType)
        except Exception:
            pass

        #: need to make a copy of the .sddraft file
        #: since StageService deletes it
        copy_location = '{}\\{}\\{}.sddraft'.format(sddraftsFolder, 'originals', locator)
        self.log.info('publishing new service')

        arcpy.Copy_management(copy_location, sddraftFile)
        self.log.info('copy done')
        arcpy.StageService_server(sddraftFile, sdFile)
        self.log.info('stage done')
        gis_server_connection = path.join(path.dirname(__file__), 'server')
        arcpy.UploadServiceDefinition_server(sdFile, gis_server_connection)
        self.log.info('upload done')

        self.log.info('validating service status')
        if (not self.agsAdmin.getStatus(service, serviceType)['realTimeState'] == 'STARTED'):
            raise '{} was not restarted successfully!'.format(service)
