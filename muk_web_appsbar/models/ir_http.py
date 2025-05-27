# from odoo import models
# from odoo.http import request


# class IrHttp(models.AbstractModel):

#     _inherit = "ir.http"

#     #----------------------------------------------------------
#     # Functions
#     #----------------------------------------------------------
    
#     def session_info(self):
#         result = super(IrHttp, self).session_info()
        
#         if request and hasattr(request, 'env') and getattr(request.env, 'user', None):
#             user = request.env.user
#             if user._is_internal():
#                 for company in user.company_ids.with_context(bin_size=True):
#                     result['user_companies']['allowed_companies'][company.id].update({
#                         'has_appsbar_image': bool(company.appbar_image),
#                     })
        
#         return result

from odoo import models
from odoo.http import request


class IrHttp(models.AbstractModel):
    _inherit = "ir.http"

    def session_info(self):
        result = super(IrHttp, self).session_info()

        # Tambahkan pengecekan yang benar-benar aman
        if request and hasattr(request, "env") and getattr(request.env, "user", False):
            user = request.env.user
            if user and user._is_internal():
                for company in user.company_ids.with_context(bin_size=True):
                    if company.id in result.get("user_companies", {}).get("allowed_companies", {}):
                        result["user_companies"]["allowed_companies"][company.id].update({
                            "has_appsbar_image": bool(company.appbar_image),
                        })

        return result
