from werkzeug import Response
from odoo import http
import json
from ..library.responses import *
from .functions import UserController


class AttendanceController(http.Controller):

    @http.route(
        "/api/attendance_sheet/", type="http", auth="user", methods=["GET"], csrf=False
    )
    def get_attendance_sheet(self, **kwargs):
        list_session: list = []

        current_user = request.env.user
        faculty_id = (
            request.env["op.faculty"]
            .sudo()
            .search([("user_id", "=", current_user.id)], limit=1)
        )
        try:
            dt_session = (
                request.env["op.session"]
                .sudo()
                .search([("faculty_id", "=", faculty_id.id)])
            )

            for session in dt_session:

                list_session.append(
                    {
                        "batch_id": session.batch_id.id,
                        "batch_name": session.batch_id.name,
                    }
                )

            return output_ok(list_session)

        except Exception as error:
            res_error = {"message": error}

            return output_bad_request(res_error)

    @http.route(
        "/api/attendance_sheet/students",
        type="http",
        auth="public",
        methods=["POST", "GET"],
        csrf=False,
    )
    def get_students_per_batch(self, **kwargs):
        list_students: list = []

        try:

            batch_id = kwargs.get("batch_id")

            qr_batch_student = """
                select os.id as id, os.full_name as full_name from op_student os join op_batch_op_student_rel obosr on os.id = obosr.op_student_id and obosr.op_batch_id = %s 
                order by os.full_name asc
            """

            cr_batch_student = request.env.cr
            cr_batch_student.execute(qr_batch_student, (batch_id,))

            columns = [desc[0] for desc in cr_batch_student.description]

            dt_student_batch = cr_batch_student.fetchall()

            res_students = [dict(zip(columns, row)) for row in dt_student_batch]

            for std in res_students:
                list_students.append(
                    {
                        "id": std.get("id"),
                        "full_name": std.get("full_name"),
                    }
                )

            return output_ok(list_students)

        except Exception as error:
            res_error = {"message": error}

            return output_bad_request(res_error)
            #INI TAMBAHAN DARI LAILA
    @http.route(
            "/api/attendance_sheet/students/<int:id>",
            type="http",
            auth="public",
            methods=["POST", "GET"],
            csrf=False,
        )
    def get_students_per_batch(self, id, **kwargs):
            list_students: list = []
            a = id
            try:

                batch_id = kwargs.get("batch_id")

                qr_batch_student = """
                    select os.id as id, os.full_name as full_name from op_student os join op_batch_op_student_rel obosr on os.id = obosr.op_student_id and obosr.op_batch_id = %s 
                    order by os.full_name asc
                """

                cr_batch_student = request.env.cr
                cr_batch_student.execute(qr_batch_student, (batch_id,))

                columns = [desc[0] for desc in cr_batch_student.description]

                dt_student_batch = cr_batch_student.fetchall()

                res_students = [dict(zip(columns, row)) for row in dt_student_batch]

                for std in res_students:
                    list_students.append(
                        {
                            "id": std.get("id"),
                            "full_name": std.get("full_name"),
                        }
                    )

                return output_ok(list_students)

            except Exception as error:
                res_error = {"message": error}

                return output_bad_request(res_error)
