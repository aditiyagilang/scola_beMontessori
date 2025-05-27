# from odoo import models
# from odoo.http import request


# class IrHttp(models.AbstractModel):

#     _inherit = "ir.http"

#     #----------------------------------------------------------
#     # Functions
#     #----------------------------------------------------------
    
#     def session_info(self):
#         result = super(IrHttp, self).session_info()
#         if request.env.user._is_internal():
#             for company in request.env.user.company_ids.with_context(bin_size=True):
#                 result['user_companies']['allowed_companies'][company.id].update({
#                     'has_background_image': bool(company.background_image),
#                 })
#         return result

from odoo import models
from odoo.http import request


class IrHttp(models.AbstractModel):
    _inherit = "ir.http"

    def session_info(self):
        result = super().session_info()

        if (
            request
            and hasattr(request, 'env')
            and getattr(request.env, 'user', None)
            and not request.env.user._is_public()
        ):
            user = request.env.user
            for company in user.company_ids.with_context(bin_size=True):
                result['user_companies']['allowed_companies'][company.id].update({
                    'has_background_image': bool(company.background_image),
                })

        return result
