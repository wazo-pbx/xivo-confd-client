# -*- coding: utf-8 -*-
# Copyright 2018 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from xivo_confd_client.crud import MultiTenantCommand


class EndpointsIAXCommand(MultiTenantCommand):

    resource = 'endpoints/iax'
