from odoo import models, fields, api, _, exceptions
from odoo.exceptions import ValidationError
from odoo.tools import safe_eval

from odoo.exceptions import ValidationError

class TaxType(models.Model):
    _name = "account.tax.type"
    _description = "Tax Type"  

    name = fields.Char(string="Name", required=True)
    description = fields.Text(string="Description")



class Taxes(models.Model):
    _inherit = "account.tax"
    _description = "Taxes"

    tax_type_id = fields.Many2one('account.tax.type', string="Tax Type")


class AccountMove(models.Model):
    _inherit = 'account.move'

    admin_state = fields.Selection(
        selection=[
            ('approve', 'Approve'),
            ('not_approve', 'Not Approve'),
        ],
        string='Admin State',
        default='not_approve',
        help="Status persetujuan admin"
    )