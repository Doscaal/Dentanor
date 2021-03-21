# copyright Doscaal 2020
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
# -*- coding: utf-8 -*-

import logging
logger = logging.getLogger('relier modele worksheet avec ceux créé à la main')


def migrate(cr, v):

    cr.execute("""UPDATE project_worksheet_template
               SET action_id = (
                    SELECT res_id
                    FROM ir_model_data
                    WHERE name = 'intervention_dentanor_action'),
                   model_id = (
                    SELECT res_id
                    FROM ir_model_data
                    WHERE name = 'model_dentanor_project_worksheet_template'),
                   report_view_id = (
                    SELECT res_id
                    FROM ir_model_data
                    WHERE name = 'report_dentanor_project_worksheet_template')
               WHERE id = (
                    SELECT res_id
                    FROM ir_model_data
                    WHERE name = 'intervention_dentanor');""")

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
