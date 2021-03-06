# -*- coding: utf-8 -*-
# Copyright 2017 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from xivo_lib_rest_client import RESTCommand
from xivo_confd_client.util import url_join


class SoundsLanguagesCommand(RESTCommand):

    resource = 'sounds/languages'

    def list(self):
        url = url_join(self.resource)
        response = self.session.get(url)
        return response.json()
