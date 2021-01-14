# coding: utf-8
#
# Copyright © Lyra Network.
# This file is part of PayZen plugin for Odoo. See COPYING.md for license details.
#
# Author:    Lyra Network (https://www.lyra.com)
# Copyright: Copyright © Lyra Network
# License:   http://www.gnu.org/licenses/agpl.html GNU Affero General Public License (AGPL v3)

import logging
import pprint

from pkg_resources import parse_version
import werkzeug

from odoo import http, release
from odoo.http import request


_logger = logging.getLogger(__name__)

class PayzenController(http.Controller):
    _notify_url = '/payment/payzen/ipn'
    _return_url = '/payment/payzen/return'

    def _get_return_url(self, result, **post):
        return_url = post.pop('return_url', '')

        if not return_url:
            if result:
                old_version = True if parse_version(release.version) < parse_version('12') else False
                return_url = '/shop/payment/validate' if old_version else '/payment/process'
            else:
                return_url = '/shop/cart'

        return return_url

    @http.route('/payment/payzen/return', type='http', auth='none', methods=['POST', 'GET'], csrf=False)
    def payzen_return(self, **post):
        _logger.info('PayZen: entering form_feedback with post data %s', pprint.pformat(post))

        # Check payment result and create transaction.
        result = request.env['payment.transaction'].sudo().form_feedback(post, 'payzen')
        return_url = self._get_return_url(result, **post)
        return werkzeug.utils.redirect(return_url)

    @http.route('/payment/payzen/ipn', type='http', auth='none', methods=['POST'], csrf=False)
    def payzen_ipn(self, **post):
        _logger.info('PayZen: entering IPN form_feedback with post data %s', pprint.pformat(post))

        # Check payment result and create transaction.
        result = request.env['payment.transaction'].sudo().form_feedback(post, 'payzen')
        return 'Accepted payment, order has been updated.' if result else 'Payment failure, order has been cancelled.'
