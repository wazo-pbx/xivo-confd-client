# -*- coding: UTF-8 -*-
# Copyright 2017 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

from xivo_lib_rest_client import RESTCommand


class VoicemailGeneralCommand(RESTCommand):

    resource = 'asterisk/voicemail/general'

    def get(self):
        response = self.session.get(self.resource)
        return response.json()

    def update(self, body):
        self.session.put(self.base_url, body)