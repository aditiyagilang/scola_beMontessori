# -*- coding: utf-8 -*-
# Part of OpenEduCat. See LICENSE file for full copyright & licensing details.

##############################################################################
#
#    OpenEduCat Inc
#    Copyright (C) 2009-TODAY OpenEduCat Inc(<https://www.openeducat.org>).
#
##############################################################################

from odoo import models, fields


class OpAcademicTerm(models.Model):

    _name = 'op.academic.term'
    _description = "Academic Term"

    name = fields.Char('Name')
    term_start_date = fields.Date('Start Date')
    term_end_date = fields.Date('End Date')
    academic_year_id = fields.Many2one(
        'op.academic.year', 'Academic Year')
    parent_term = fields.Many2one('op.academic.term', 'Parent Term')
    company_id = fields.Many2one(
        'res.company', string='Company',
        default=lambda self: self.env.user.company_id)
