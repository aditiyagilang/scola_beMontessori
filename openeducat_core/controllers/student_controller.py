from werkzeug import Response
from odoo import http
import json
from ..library.responses import *


class StudentController(http.Controller):

    @http.route(
        "/api/get_students/", type="http", auth="user", methods=["GET"], csrf=False
    )
    def get_students(self, **kwargs):
        students = http.request.env["op.student"].search([])

        student_data: list = []
        output: dict = {}
        for student in students:
            student_data.append(
                {
                    "id": student.id,
                    "name": student.name,
                    "gender": student.gender,
                    "birth_date": str(student.birth_date),
                }
            )
            output = {"results": {"code": 200, "message": "OK", "data": student_data}}

        return Response(
            json.dumps(output), headers={"Content-Type": "application/json"}
        )

    def authenticate_token(self):
        IrHttp = request.env["ir.http"].sudo()
        IrHttp._auth_method_outlook()
