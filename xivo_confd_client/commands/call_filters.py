# -*- coding: utf-8 -*-
# Copyright 2018 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

from xivo_confd_client.crud import CRUDCommand
from xivo_confd_client.relations import (
    CallFilterFallbackRelation,
    CallFilterRecipientUserRelation,
    CallFilterSurrogateUserRelation,
)


class CallFilterRelation(object):

    def __init__(self, builder, call_filter_id):
        self.call_filter_id = call_filter_id
        self.call_filter_user_recipients = CallFilterRecipientUserRelation(builder)
        self.call_filter_user_surrogates = CallFilterSurrogateUserRelation(builder)
        self.call_filter_fallback = CallFilterFallbackRelation(builder)

    def update_user_surrogates(self, users):
        return self.call_filter_user_surrogates.associate(self.call_filter_id, users)

    def update_user_recipients(self, users):
        return self.call_filter_user_recipients.associate(self.call_filter_id, users)

    def update_fallbacks(self, fallbacks):
        self.call_filter_fallback.update_fallbacks(self.call_filter_id, fallbacks)


class CallFiltersCommand(CRUDCommand):

    resource = 'callfilters'
    relation_cmd = CallFilterRelation