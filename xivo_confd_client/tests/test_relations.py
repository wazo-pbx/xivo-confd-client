# -*- coding: UTF-8 -*-

# Copyright 2015-2017 The Wazo Authors  (see the AUTHORS file)
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.


from hamcrest import assert_that

from xivo_confd_client.tests import TestCommand
from xivo_confd_client.relations import (ConferenceExtensionRelation,
                                         GroupExtensionRelation,
                                         GroupFallbackRelation,
                                         GroupMemberUserRelation,
                                         IncallExtensionRelation,
                                         LineDeviceRelation,
                                         LineEndpointCustomRelation,
                                         LineEndpointSccpRelation,
                                         LineEndpointSipRelation,
                                         LineExtensionRelation,
                                         OutcallExtensionRelation,
                                         OutcallTrunkRelation,
                                         PagingCallerUserRelation,
                                         PagingMemberUserRelation,
                                         ParkingLotExtensionRelation,
                                         TrunkEndpointCustomRelation,
                                         TrunkEndpointSipRelation,
                                         UserCallPermissionRelation,
                                         UserCtiProfileRelation,
                                         UserEntityRelation,
                                         UserFallbackRelation,
                                         UserForwardRelation,
                                         UserFuncKeyRelation,
                                         UserLineRelation,
                                         UserServiceRelation,
                                         UserAgentRelation,
                                         UserEndpointSipRelation,
                                         UserVoicemailRelation)


class TestUserLineRelation(TestCommand):

    Command = UserLineRelation

    def test_user_line_association(self):
        user_id = 1
        line_id = 2

        self.command.associate(user_id, line_id)
        self.session.put.assert_called_once_with("/users/1/lines/2")

    def test_user_line_dissociation(self):
        user_id = 1
        line_id = 2

        self.command.dissociate(user_id, line_id)
        self.session.delete.assert_called_once_with("/users/1/lines/2")

    def test_user_line_list_by_user(self):
        user_id = 1234
        expected_url = "/users/{}/lines".format(user_id)
        expected_result = {
            "total": 0,
            "items": []
        }

        self.set_response('get', 200, expected_result)

        result = self.command.list_by_user(user_id)

        self.session.get.assert_called_once_with(expected_url)
        assert_that(result, expected_result)

    def test_user_line_list_by_line(self):
        line_id = 1234
        expected_url = "/lines/{}/users".format(line_id)
        expected_result = {
            "total": 0,
            "items": []
        }

        self.set_response('get', 200, expected_result)

        result = self.command.list_by_line(line_id)

        self.session.get.assert_called_once_with(expected_url)
        assert_that(result, expected_result)


class TestUserEndpointSipRelation(TestCommand):

    Command = UserEndpointSipRelation

    def test_user_line_list_by_user(self):
        user_uuid = '1234-abcd'
        line_id = 42
        expected_url = "/users/{}/lines/{}/associated/endpoints/sip".format(user_uuid, line_id)
        expected_result = {"username": 'tata'}

        self.set_response('get', 200, expected_result)

        result = self.command.get_by_user_line(user_uuid, line_id)

        self.session.get.assert_called_once_with(expected_url)
        assert_that(result, expected_result)


class TestLineExtensionRelation(TestCommand):

    Command = LineExtensionRelation

    def test_line_extension_association(self):
        line_id = 1
        extension_id = 2

        self.command.associate(line_id, extension_id)
        self.session.put.assert_called_once_with("/lines/1/extensions/2")

    def test_line_extension_dissociation(self):
        line_id = 1
        extension_id = 2

        self.command.dissociate(line_id, extension_id)
        self.session.delete.assert_called_once_with("/lines/1/extensions/2")

    def test_list_by_line(self):
        line_id = 1
        extension_id = 2

        expected_result = {
            'total': 1,
            'items': [{
                'line_id': line_id,
                'extension_id': extension_id,
                'links': [
                    {'rel': 'lines',
                     'href': 'http://localhost:9486/1.1/lines/1'},
                    {'rel': 'extensions',
                     'href': 'http://localhost:9486/1.1/extensions/2'},
                ]}
            ]
        }

        self.set_response('get', 200, expected_result)

        response = self.command.list_by_line(line_id)
        self.session.get.assert_called_once_with("/lines/1/extensions")

        assert_that(response, expected_result)

    def test_list_by_extension(self):
        line_id = 1
        extension_id = 2

        expected_result = {
            'total': 1,
            'items': [{
                'line_id': line_id,
                'extension_id': extension_id,
                'links': [
                    {'rel': 'lines',
                     'href': 'http://localhost:9486/1.1/lines/1'},
                    {'rel': 'extensions',
                     'href': 'http://localhost:9486/1.1/extensions/2'},
                ]}
            ]
        }

        self.set_response('get', 200, expected_result)

        response = self.command.list_by_extension(extension_id)
        self.session.get.assert_called_once_with("/extensions/2/lines")

        assert_that(response, expected_result)

    def test_get_by_extension(self):
        line_id = 1
        extension_id = 2

        expected_result = {
            'line_id': line_id,
            'extension_id': extension_id,
            'links': [
                {'rel': 'lines',
                 'href': 'http://localhost:9486/1.1/lines/1'},
                {'rel': 'extensions',
                 'href': 'http://localhost:9486/1.1/extensions/2'},
            ]
        }

        self.set_response('get', 200, expected_result)

        response = self.command.get_by_extension(extension_id)
        self.session.get.assert_called_once_with("/extensions/2/line")

        assert_that(response, expected_result)


class TestLineDeviceRelation(TestCommand):

    Command = LineDeviceRelation

    def test_line_device_association(self):
        line_id = 1
        device_id = 2

        self.set_response('put', 204)

        self.command.associate(line_id, device_id)
        self.session.put.assert_called_once_with("/lines/1/devices/2")

    def test_line_device_dissociation(self):
        line_id = 1
        device_id = 2

        self.set_response('delete', 204)

        self.command.dissociate(line_id, device_id)
        self.session.delete.assert_called_once_with("/lines/1/devices/2")

    def test_get_by_line(self):
        line_id = 1
        device_id = 2

        expected_result = {
            'line_id': line_id,
            'device_id': device_id,
            'links': [
                {'rel': 'lines',
                 'href': 'http://localhost:9486/1.1/lines/1'},
                {'rel': 'devices',
                 'href': 'http://localhost:9486/1.1/devices/1'},
            ]
        }

        self.set_response('get', 200, expected_result)

        response = self.command.get_by_line(line_id)
        self.session.get.assert_called_once_with("/lines/1/devices")

        assert_that(response, expected_result)

    def test_list_by_device(self):
        line_id = 1
        device_id = 2

        expected_result = {'total': 1,
                           'items': [
                               {'line_id': line_id,
                                'device_id': device_id,
                                'links': [
                                    {'rel': 'lines',
                                     'href': 'http://localhost:9486/1.1/lines/1'},
                                    {'rel': 'devices',
                                     'href': 'http://localhost:9486/1.1/devices/1'},
                                ]}]}

        self.set_response('get', 200, expected_result)

        response = self.command.list_by_device(device_id)
        self.session.get.assert_called_once_with("/devices/2/lines")

        assert_that(response, expected_result)


class TestLineEndpointSipRelation(TestCommand):

    Command = LineEndpointSipRelation

    def test_line_endpoint_sip_association(self):
        line_id = 1
        sip_id = 2

        self.set_response('put', 204)

        self.command.associate(line_id, sip_id)
        self.session.put.assert_called_once_with("/lines/1/endpoints/sip/2")

    def test_line_endpoint_sip_dissociation(self):
        line_id = 1
        sip_id = 2

        self.set_response('delete', 204)

        self.command.dissociate(line_id, sip_id)
        self.session.delete.assert_called_once_with("/lines/1/endpoints/sip/2")

    def test_get_by_line(self):
        line_id = 1
        sip_id = 2

        expected_result = {
            'line_id': line_id,
            'sip_id': sip_id,
            'links': [
                {'rel': 'lines',
                 'href': 'http://localhost:9486/1.1/lines/1'},
                {'rel': 'endpoints_sip',
                 'href': 'http://localhost:9486/1.1/endpoints/sip/1'},
            ]
        }

        self.set_response('get', 200, expected_result)

        response = self.command.get_by_line(line_id)
        self.session.get.assert_called_once_with("/lines/1/endpoints/sip")

        assert_that(response, expected_result)

    def test_get_by_endpoint_sip(self):
        line_id = 1
        sip_id = 2

        expected_result = {
            'line_id': line_id,
            'sip_id': sip_id,
            'links': [
                {'rel': 'lines',
                 'href': 'http://localhost:9486/1.1/lines/1'},
                {'rel': 'endpoints_sip',
                 'href': 'http://localhost:9486/1.1/endpoints/sip/1'},
            ]
        }

        self.set_response('get', 200, expected_result)

        response = self.command.get_by_endpoint_sip(sip_id)
        self.session.get.assert_called_once_with("/endpoints/sip/2/lines")

        assert_that(response, expected_result)


class TestLineEndpointSccpRelation(TestCommand):

    Command = LineEndpointSccpRelation

    def test_line_endpoint_sccp_association(self):
        line_id = 1
        sccp_id = 2

        self.set_response('put', 204)

        self.command.associate(line_id, sccp_id)
        self.session.put.assert_called_once_with("/lines/1/endpoints/sccp/2")

    def test_line_endpoint_sccp_dissociation(self):
        line_id = 1
        sccp_id = 2

        self.set_response('delete', 204)

        self.command.dissociate(line_id, sccp_id)
        self.session.delete.assert_called_once_with("/lines/1/endpoints/sccp/2")

    def test_get_by_line(self):
        line_id = 1
        sccp_id = 2

        expected_result = {
            'line_id': line_id,
            'sccp_id': sccp_id,
            'links': [
                {'rel': 'lines',
                 'href': 'http://localhost:9486/1.1/lines/1'},
                {'rel': 'endpoints_sccp',
                 'href': 'http://localhost:9486/1.1/endpoints/sccp/1'},
            ]
        }

        self.set_response('get', 200, expected_result)

        response = self.command.get_by_line(line_id)
        self.session.get.assert_called_once_with("/lines/1/endpoints/sccp")

        assert_that(response, expected_result)

    def test_get_by_endpoint_sccp(self):
        line_id = 1
        sccp_id = 2

        expected_result = {
            'line_id': line_id,
            'sccp_id': sccp_id,
            'links': [
                {'rel': 'lines',
                 'href': 'http://localhost:9486/1.1/lines/1'},
                {'rel': 'endpoints_sccp',
                 'href': 'http://localhost:9486/1.1/endpoints/sccp/1'},
            ]
        }

        self.set_response('get', 200, expected_result)

        response = self.command.get_by_endpoint_sccp(sccp_id)
        self.session.get.assert_called_once_with("/endpoints/sccp/2/lines")

        assert_that(response, expected_result)


class TestLineEndpointCustomRelation(TestCommand):

    Command = LineEndpointCustomRelation

    def test_line_endpoint_custom_association(self):
        line_id = 1
        custom_id = 2

        self.set_response('put', 204)

        self.command.associate(line_id, custom_id)
        self.session.put.assert_called_once_with("/lines/1/endpoints/custom/2")

    def test_line_endpoint_custom_dissociation(self):
        line_id = 1
        custom_id = 2

        self.set_response('delete', 204)

        self.command.dissociate(line_id, custom_id)
        self.session.delete.assert_called_once_with("/lines/1/endpoints/custom/2")

    def test_get_by_line(self):
        line_id = 1
        custom_id = 2

        expected_result = {
            'line_id': line_id,
            'custom_id': custom_id,
            'links': [
                {'rel': 'lines',
                 'href': 'http://localhost:9486/1.1/lines/1'},
                {'rel': 'endpoints_custom',
                 'href': 'http://localhost:9486/1.1/endpoints/custom/1'},
            ]
        }

        self.set_response('get', 200, expected_result)

        response = self.command.get_by_line(line_id)
        self.session.get.assert_called_once_with("/lines/1/endpoints/custom")

        assert_that(response, expected_result)

    def test_get_by_endpoint_custom(self):
        line_id = 1
        custom_id = 2

        expected_result = {
            'line_id': line_id,
            'custom_id': custom_id,
            'links': [
                {'rel': 'lines',
                 'href': 'http://localhost:9486/1.1/lines/1'},
                {'rel': 'endpoints_custom',
                 'href': 'http://localhost:9486/1.1/endpoints/custom/1'},
            ]
        }

        self.set_response('get', 200, expected_result)

        response = self.command.get_by_endpoint_custom(custom_id)
        self.session.get.assert_called_once_with("/endpoints/custom/2/lines")

        assert_that(response, expected_result)


class TestUserVoicemailRelation(TestCommand):

    Command = UserVoicemailRelation

    def test_user_voicemail_association(self):
        user_id = 1
        voicemail_id = 2

        self.command.associate(user_id, voicemail_id)
        self.session.put.assert_called_once_with("/users/1/voicemails/2")

    def test_user_voicemail_dissociation(self):
        user_id = 1

        self.command.dissociate(user_id)
        self.session.delete.assert_called_once_with("/users/1/voicemails")

    def test_get_by_user(self):
        user_id = 1
        expected_result = {
            'user_id': user_id,
            'voicemail_id': 2,
            'links': [
                {'rel': 'users',
                 'href': 'http://localhost:9486/1.1/users/1'},
                {'rel': 'voicemails',
                 'href': 'http://localhost:9486/1.1/voicemails/2'},
            ]
        }

        self.set_response('get', 200, expected_result)

        response = self.command.get_by_user(user_id)

        self.session.get.assert_called_once_with("/users/1/voicemails")
        assert_that(response, expected_result)

    def test_list_by_voicemail(self):
        voicemail_id = 1
        expected_result = {
            'items': [],
            'total': 0
        }

        self.set_response('get', 200, expected_result)

        response = self.command.list_by_voicemail(voicemail_id)

        self.session.get.assert_called_once_with("/voicemails/1/users")
        assert_that(response, expected_result)


class TestUserAgentRelation(TestCommand):

    Command = UserAgentRelation

    def test_user_agent_association(self):
        user_id = 1
        agent_id = 2

        self.command.associate(user_id, agent_id)
        self.session.put.assert_called_once_with("/users/1/agents/2")

    def test_user_agent_dissociation(self):
        user_id = 1

        self.command.dissociate(user_id)
        self.session.delete.assert_called_once_with("/users/1/agents")

    def test_get_by_user(self):
        user_id = 1
        expected_result = {
            'user_id': user_id,
            'agent_id': 2,
            'links': [
                {'rel': 'users',
                 'href': 'http://localhost:9486/1.1/users/1'},
                {'rel': 'agents',
                 'href': 'http://localhost:9486/1.1/agents/2'},
            ]
        }

        self.set_response('get', 200, expected_result)

        response = self.command.get_by_user(user_id)

        self.session.get.assert_called_once_with("/users/1/agents")
        assert_that(response, expected_result)


class TestUserFuncKeyRelation(TestCommand):

    Command = UserFuncKeyRelation

    def test_update_func_key(self):
        user_id = 1234
        position = 1
        funckey = {'destination': {'type': 'service', 'service': 'enablednd'}}

        self.command.update_funckey(user_id, position, funckey)

        expected_url = "/users/{}/funckeys/{}".format(user_id, position)
        self.session.put.assert_called_with(expected_url, funckey)

    def test_remove_func_key(self):
        user_id = 1234
        position = 1
        expected_url = "/users/{}/funckeys/{}".format(user_id, position)

        self.command.remove_funckey(user_id, position)

        self.session.delete.assert_called_with(expected_url)

    def test_list_funckeys(self):
        user_id = 1234
        expected_url = "/users/{}/funckeys".format(user_id)
        expected_result = {
            "total": 0,
            "items": []
        }

        self.set_response('get', 200, expected_result)

        result = self.command.list_funckeys(user_id)

        self.session.get.assert_called_once_with(expected_url)
        assert_that(result, expected_result)

    def test_get_funckey(self):
        user_id = 1234
        position = 3
        expected_url = "/users/{}/funckeys/{}".format(user_id, position)
        expected_result = {
            "blf": True,
            "label": "Call john",
            "destination": {
                "type": "user",
                "user_id": 34
            }
        }

        self.set_response('get', 200, expected_result)

        result = self.command.get_funckey(user_id, position)

        self.session.get.assert_called_once_with(expected_url)
        assert_that(result, expected_result)

    def test_update_funckeys(self):
        user_id = 1234
        funckeys = {'keys': {'1': {'destination': {'type': 'service', 'service': 'enablednd'}},
                             '2': {'destination': {'type': 'custom', 'exten': '1234'}}}}

        self.command.update_funckeys(user_id, funckeys)

        expected_url = "/users/{}/funckeys".format(user_id)
        self.session.put.assert_called_with(expected_url, funckeys)

    def test_dissociate_funckey_template(self):
        user_id = 1234
        template_id = 25
        expected_url = "/users/{}/funckeys/templates/{}".format(user_id, template_id)

        self.set_response('delete', 204)

        self.command.dissociate_funckey_template(user_id, template_id)

        self.session.delete.assert_called_once_with(expected_url)

    def test_associate_funckey_template(self):
        user_id = 1234
        template_id = 25
        expected_url = "/users/{}/funckeys/templates/{}".format(user_id, template_id)

        self.set_response('put', 204)

        self.command.associate_funckey_template(user_id, template_id)

        self.session.put.assert_called_once_with(expected_url)


class TestUserCtiProfileRelation(TestCommand):

    Command = UserCtiProfileRelation

    def test_get_by_user(self):
        user_id = 1234
        expected_url = "/users/{}/cti".format(user_id)
        expected_result = {
            'cti_profile_id': 2345,
            'enabled': True,
            'user_id': user_id
        }

        self.set_response('get', 200, expected_result)

        result = self.command.get_by_user(user_id)

        self.session.get.assert_called_once_with(expected_url)
        assert_that(result, expected_result)

    def test_associate(self):
        user_id = 1234
        cti_profile_id = 2345

        expected_url = "/users/{}/cti".format(user_id)
        expected_body = {
            'cti_profile_id': 2345,
            'enabled': True,
        }

        self.set_response('put', 204)

        self.command.associate(user_id, cti_profile_id)

        self.session.put.assert_called_once_with(expected_url, expected_body)

    def test_disable(self):
        user_id = 1234

        expected_url = "/users/{}/cti".format(user_id)
        expected_body = {
            'enabled': False,
        }

        self.set_response('put', 204)

        self.command.disable(user_id)

        self.session.put.assert_called_once_with(expected_url, expected_body)


class TestUserServiceRelation(TestCommand):

    Command = UserServiceRelation

    def test_update_service(self):
        user_id = 1234
        service_name = 'dnd'
        service = {'enabled': True}

        self.command.update_service(user_id, service_name, service)

        expected_url = "/users/{}/services/{}".format(user_id, service_name)
        self.session.put.assert_called_with(expected_url, service)

    def test_get_service(self):
        user_id = 1234
        service_name = 'dnd'
        expected_url = "/users/{}/services/{}".format(user_id, service_name)
        expected_result = {'enabled': True}

        self.set_response('get', 200, expected_result)

        result = self.command.get_service(user_id, service_name)

        self.session.get.assert_called_once_with(expected_url)
        assert_that(result, expected_result)

    def test_list_services(self):
        user_id = 1234
        expected_url = "/users/{}/services".format(user_id)
        expected_result = {
            "total": 0,
            "items": []
        }

        self.set_response('get', 200, expected_result)

        result = self.command.list_services(user_id)

        self.session.get.assert_called_once_with(expected_url)
        assert_that(result, expected_result)


class TestUserForwardRelation(TestCommand):

    Command = UserForwardRelation

    def test_update_forward(self):
        user_id = 1234
        forward_name = 'dnd'
        forward = {'enabled': True}

        self.command.update_forward(user_id, forward_name, forward)

        expected_url = "/users/{}/forwards/{}".format(user_id, forward_name)
        self.session.put.assert_called_with(expected_url, forward)

    def test_get_forward(self):
        user_id = 1234
        forward_name = 'dnd'
        expected_url = "/users/{}/forwards/{}".format(user_id, forward_name)
        expected_result = {'enabled': True}

        self.set_response('get', 200, expected_result)

        result = self.command.get_forward(user_id, forward_name)

        self.session.get.assert_called_once_with(expected_url)
        assert_that(result, expected_result)

    def test_list_forwards(self):
        user_id = 1234
        expected_url = "/users/{}/forwards".format(user_id)
        expected_result = {
            "total": 0,
            "items": []
        }

        self.set_response('get', 200, expected_result)

        result = self.command.list_forwards(user_id)

        self.session.get.assert_called_once_with(expected_url)
        assert_that(result, expected_result)

    def test_update_forwards(self):
        user_id = 1234
        forwards = {'busy': {'enabled': True, 'destination': '123'},
                    'noanswer': {'enabled': False, 'destination': '456'},
                    'unconditional': {'enabled': False, 'destination': None}}

        self.command.update_forwards(user_id, forwards)

        expected_url = "/users/{}/forwards".format(user_id)
        self.session.put.assert_called_with(expected_url, forwards)


class TestUserCallPermissionRelation(TestCommand):

    Command = UserCallPermissionRelation

    def test_user_call_permission_association(self):
        user_id = 1
        call_permission_id = 2

        self.command.associate(user_id, call_permission_id)
        self.session.put.assert_called_once_with("/users/1/callpermissions/2")

    def test_user_call_permission_dissociation(self):
        user_id = 1
        call_permission_id = 2

        self.command.dissociate(user_id, call_permission_id)
        self.session.delete.assert_called_once_with("/users/1/callpermissions/2")

    def test_user_call_permission_list_by_user(self):
        user_id = 1234
        expected_url = "/users/{}/callpermissions".format(user_id)
        expected_result = {
            "total": 0,
            "items": []
        }

        self.set_response('get', 200, expected_result)

        result = self.command.list_by_user(user_id)

        self.session.get.assert_called_once_with(expected_url)
        assert_that(result, expected_result)

    def test_user_call_permission_list_by_call_permission(self):
        call_permission_id = 1234
        expected_url = "/callpermissions/{}/users".format(call_permission_id)
        expected_result = {
            "total": 0,
            "items": []
        }

        self.set_response('get', 200, expected_result)

        result = self.command.list_by_call_permission(call_permission_id)

        self.session.get.assert_called_once_with(expected_url)
        assert_that(result, expected_result)


class TestEntityRelation(TestCommand):

    Command = UserEntityRelation

    def test_user_entity_association(self):
        user_id = 1
        entity_id = 2

        self.command.associate(user_id, entity_id)
        self.session.put.assert_called_once_with("/users/1/entities/2")

    def test_user_entity_list_by_user(self):
        user_id = 1234
        expected_url = "/users/{}/entities".format(user_id)
        expected_result = {'entity_id': '1',
                           'user_id': '2'}

        self.set_response('get', 200, expected_result)

        result = self.command.get_by_user(user_id)

        self.session.get.assert_called_once_with(expected_url)
        assert_that(result, expected_result)


class TestTrunkEndpointSipRelation(TestCommand):

    Command = TrunkEndpointSipRelation

    def test_trunk_endpoint_sip_association(self):
        trunk_id = 1
        sip_id = 2

        self.set_response('put', 204)

        self.command.associate(trunk_id, sip_id)
        self.session.put.assert_called_once_with("/trunks/1/endpoints/sip/2")

    def test_trunk_endpoint_sip_dissociation(self):
        trunk_id = 1
        sip_id = 2

        self.set_response('delete', 204)

        self.command.dissociate(trunk_id, sip_id)
        self.session.delete.assert_called_once_with("/trunks/1/endpoints/sip/2")

    def test_get_by_trunk(self):
        trunk_id = 1
        sip_id = 2

        expected_result = {'trunk_id': trunk_id,
                           'endpoint_id': sip_id}

        self.set_response('get', 200, expected_result)

        response = self.command.get_by_trunk(trunk_id)
        self.session.get.assert_called_once_with("/trunks/1/endpoints/sip")

        assert_that(response, expected_result)

    def test_get_by_endpoint_sip(self):
        trunk_id = 1
        sip_id = 2

        expected_result = {'trunk_id': trunk_id,
                           'endpoint_id': sip_id}

        self.set_response('get', 200, expected_result)

        response = self.command.get_by_endpoint_sip(sip_id)
        self.session.get.assert_called_once_with("/endpoints/sip/2/trunks")

        assert_that(response, expected_result)


class TestTrunkEndpointCustomRelation(TestCommand):

    Command = TrunkEndpointCustomRelation

    def test_trunk_endpoint_custom_association(self):
        trunk_id = 1
        custom_id = 2

        self.set_response('put', 204)

        self.command.associate(trunk_id, custom_id)
        self.session.put.assert_called_once_with("/trunks/1/endpoints/custom/2")

    def test_trunk_endpoint_custom_dissociation(self):
        trunk_id = 1
        custom_id = 2

        self.set_response('delete', 204)

        self.command.dissociate(trunk_id, custom_id)
        self.session.delete.assert_called_once_with("/trunks/1/endpoints/custom/2")

    def test_get_by_trunk(self):
        trunk_id = 1
        custom_id = 2

        expected_result = {'trunk_id': trunk_id,
                           'endpoint_id': custom_id}

        self.set_response('get', 200, expected_result)

        response = self.command.get_by_trunk(trunk_id)
        self.session.get.assert_called_once_with("/trunks/1/endpoints/custom")

        assert_that(response, expected_result)

    def test_get_by_endpoint_custom(self):
        trunk_id = 1
        custom_id = 2

        expected_result = {'trunk_id': trunk_id,
                           'endpoint_id': custom_id}

        self.set_response('get', 200, expected_result)

        response = self.command.get_by_endpoint_custom(custom_id)
        self.session.get.assert_called_once_with("/endpoints/custom/2/trunks")

        assert_that(response, expected_result)


class TestIncallExtensionRelation(TestCommand):

    Command = IncallExtensionRelation

    def test_incall_extension_association(self):
        incall_id = 1
        extension_id = 2

        self.set_response('put', 204)

        self.command.associate(incall_id, extension_id)
        self.session.put.assert_called_once_with("/incalls/1/extensions/2")

    def test_incall_extension_dissociation(self):
        incall_id = 1
        extension_id = 2

        self.set_response('delete', 204)

        self.command.dissociate(incall_id, extension_id)
        self.session.delete.assert_called_once_with("/incalls/1/extensions/2")


class TestOutcallTrunkRelation(TestCommand):

    Command = OutcallTrunkRelation

    def test_outcall_trunk_association(self):
        outcall_id = 1
        trunks = [{'id': 2}, {'id': 3}]

        self.set_response('put', 204)
        expected_body = {'trunks': trunks}

        self.command.associate(outcall_id, trunks)
        self.session.put.assert_called_once_with("/outcalls/1/trunks", expected_body)


class TestOutcallExtensionRelation(TestCommand):

    Command = OutcallExtensionRelation

    def test_outcall_extension_association(self):
        outcall_id = 1
        extension_id = 2

        self.set_response('put', 204)
        expected_body = {'prefix': '123',
                         'external_prefix': '456',
                         'strip_digits': 2,
                         'caller_id': 'toto'}

        self.command.associate(outcall_id, extension_id,
                               prefix='123',
                               external_prefix='456',
                               strip_digits=2,
                               caller_id='toto')
        self.session.put.assert_called_once_with("/outcalls/1/extensions/2", expected_body)

    def test_outcall_extension_dissociation(self):
        outcall_id = 1
        extension_id = 2

        self.set_response('delete', 204)

        self.command.dissociate(outcall_id, extension_id)
        self.session.delete.assert_called_once_with("/outcalls/1/extensions/2")


class TestGroupExtensionRelation(TestCommand):

    Command = GroupExtensionRelation

    def test_group_extension_association(self):
        group_id = 1
        extension_id = 2

        self.set_response('put', 204)

        self.command.associate(group_id, extension_id)
        self.session.put.assert_called_once_with("/groups/1/extensions/2")

    def test_group_extension_dissociation(self):
        group_id = 1
        extension_id = 2

        self.set_response('delete', 204)

        self.command.dissociate(group_id, extension_id)
        self.session.delete.assert_called_once_with("/groups/1/extensions/2")


class TestGroupMemberUserRelation(TestCommand):

    Command = GroupMemberUserRelation

    def test_group_user_association(self):
        group_id = 1
        users = [{'uuid': 'a-2'}, {'uuid': 'b-3'}]

        self.set_response('put', 204)
        expected_body = {'users': users}

        self.command.associate(group_id, users)
        self.session.put.assert_called_once_with("/groups/1/members/users", expected_body)


class TestGroupFallbackRelation(TestCommand):

    Command = GroupFallbackRelation

    def test_list_fallbacks(self):
        group_id = 1234
        expected_url = "/groups/{}/fallbacks".format(group_id)
        expected_result = {'noanswer_destination': {'type': 'none'}}

        self.set_response('get', 200, expected_result)

        result = self.command.list_fallbacks(group_id)

        self.session.get.assert_called_once_with(expected_url)
        assert_that(result, expected_result)

    def test_update_fallbacks(self):
        group_id = 1234
        fallbacks = {'noanswer_destination': {'type': 'none'}}

        self.command.update_fallbacks(group_id, fallbacks)

        expected_url = "/groups/{}/fallbacks".format(group_id)
        self.session.put.assert_called_with(expected_url, fallbacks)


class TestUserFallbackRelation(TestCommand):

    Command = UserFallbackRelation

    def test_list_fallbacks(self):
        user_id = 1234
        expected_url = "/users/{}/fallbacks".format(user_id)
        expected_result = {'noanswer_destination': None,
                           'busy_destination': None,
                           'congestion_destination': None,
                           'fail_destination': None}

        self.set_response('get', 200, expected_result)

        result = self.command.list_fallbacks(user_id)

        self.session.get.assert_called_once_with(expected_url)
        assert_that(result, expected_result)

    def test_update_fallbacks(self):
        user_id = 1234
        fallbacks = {'noanswer_destination': None,
                     'busy_destination': None,
                     'congestion_destination': None,
                     'fail_destination': None}

        self.command.update_fallbacks(user_id, fallbacks)

        expected_url = "/users/{}/fallbacks".format(user_id)
        self.session.put.assert_called_with(expected_url, fallbacks)


class TestConferenceExtensionRelation(TestCommand):

    Command = ConferenceExtensionRelation

    def test_conference_extension_association(self):
        conference_id = 1
        extension_id = 2

        self.set_response('put', 204)

        self.command.associate(conference_id, extension_id)
        self.session.put.assert_called_once_with("/conferences/1/extensions/2")

    def test_conference_extension_dissociation(self):
        conference_id = 1
        extension_id = 2

        self.set_response('delete', 204)

        self.command.dissociate(conference_id, extension_id)
        self.session.delete.assert_called_once_with("/conferences/1/extensions/2")


class TestParkingLotExtensionRelation(TestCommand):

    Command = ParkingLotExtensionRelation

    def test_parking_lot_extension_association(self):
        parking_lot_id = 1
        extension_id = 2

        self.set_response('put', 204)

        self.command.associate(parking_lot_id, extension_id)
        self.session.put.assert_called_once_with("/parkinglots/1/extensions/2")

    def test_parking_lot_extension_dissociation(self):
        parking_lot_id = 1
        extension_id = 2

        self.set_response('delete', 204)

        self.command.dissociate(parking_lot_id, extension_id)
        self.session.delete.assert_called_once_with("/parkinglots/1/extensions/2")


class TestPagingMemberUserRelation(TestCommand):

    Command = PagingMemberUserRelation

    def test_paging_user_association(self):
        paging_id = 1
        users = [{'uuid': 'a-2'}, {'uuid': 'b-3'}]

        self.set_response('put', 204)
        expected_body = {'users': users}

        self.command.associate(paging_id, users)
        self.session.put.assert_called_once_with("/pagings/1/members/users", expected_body)


class TestPagingCallerUserRelation(TestCommand):

    Command = PagingCallerUserRelation

    def test_paging_user_association(self):
        paging_id = 1
        users = [{'uuid': 'a-2'}, {'uuid': 'b-3'}]

        self.set_response('put', 204)
        expected_body = {'users': users}

        self.command.associate(paging_id, users)
        self.session.put.assert_called_once_with("/pagings/1/callers/users", expected_body)
