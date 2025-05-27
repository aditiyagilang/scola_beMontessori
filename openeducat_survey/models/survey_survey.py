from odoo import models, fields, api, _, exceptions
import uuid
from odoo.exceptions import ValidationError

from odoo import models, fields, api
from odoo.tools import safe_eval

from odoo.exceptions import ValidationError

class SurveySurvey(models.Model):
    _inherit = "survey.survey"

    is_quiz = fields.Boolean("Is Quiz", default=False, help="Check if this is a quiz")

    batch_id = fields.Many2one('op.batch', string='Batch', help="Select related batch", 
                               domain="[('active', '=', True)]", required=False)

    exam_id = fields.Many2one('op.exam', string='Exam', help="Related Exam")
    course_id = fields.Many2one('op.course', string='Course', help="Related Course")

    status = fields.Selection([
        ('start', 'Start'),
        ('on_going', 'On Going'),
        ('finish', 'Finish')
    ], string='Status', default='start', tracking=True)

    url_link = fields.Char("Survey Link", compute="_compute_url_link", store=True)

    start_datetime = fields.Datetime("Start Date", help="Start time of the quiz", required=False)
    end_datetime = fields.Datetime("End Date", help="End time of the quiz", required=False)

    @api.constrains('is_quiz', 'start_datetime', 'end_datetime')
    def _check_quiz_dates(self):
        """ Pastikan start_datetime dan end_datetime wajib diisi jika is_quiz = True """
        for record in self:
            if record.is_quiz and (not record.start_datetime or not record.end_datetime):
                raise ValidationError("Jika ini adalah quiz, Start Date dan End Date harus diisi!")

    @api.onchange('is_quiz')
    def _onchange_is_quiz(self):
        """ Jika is_quiz tidak dicentang, hapus nilai start_datetime & end_datetime """
        if not self.is_quiz:
            self.start_datetime = False
            self.end_datetime = False


    @api.model
    def create(self, vals):
        """ Override create untuk memastikan _create_student_exam_entries dipanggil setelah entri dibuat """
        record = super(SurveySurvey, self).create(vals)

        if record.is_quiz and record.batch_id:
            record._create_student_exam_entries()

        return record

    def write(self, vals):
        """ Override write untuk memastikan _create_student_exam_entries dipanggil setelah data diperbarui """
        res = super(SurveySurvey, self).write(vals)

        if 'is_quiz' in vals and self.is_quiz and self.batch_id:
            self._create_student_exam_entries()

        return res

    @api.model
    def _create_student_exam_entries(self):
        """ Tambahkan entri student_user_exam untuk setiap mahasiswa dalam batch """
        if self.is_quiz and self.batch_id:
            self.env.cr.execute("""
                SELECT op_student_id
                FROM op_batch_op_student_rel
                WHERE op_batch_id = %s
            """, (self.batch_id.id,))

            student_ids = self.env.cr.fetchall()

            if not student_ids:
                raise ValidationError("Tidak ada siswa yang ditemukan dalam batch ini.")

            student_exam_model = self.env['student_user_exam']  
            for student_id in student_ids:
                student_exam_model.create({
                    'student_id': student_id[0],  
                    'batch_id': self.batch_id.id,
                    'exam_id': False,  
                    'survey_id': self.id,
                })



    @api.constrains('course_id')
    def _check_course_id(self):
        for record in self:
            if not record.course_id:
                raise exceptions.ValidationError("Survey harus memiliki Course!")

    @api.depends('status')
    def _compute_url_link(self):
        """Generate unique survey URL when status is 'on_going'."""
        for record in self:
            if record.status == 'on_going' and not record.url_link:
                record.url_link = f"/survey/start/{uuid.uuid4()}"
            elif record.status == 'finish':
                record.url_link = False  

    def open_survey(self):
        """Prevent access if survey is not in 'on_going' status."""
        if self.status != 'on_going' or not self.url_link:
            raise ValidationError(_("Survey is not available to be answered."))
        return {
            'type': 'ir.actions.act_url',
            'url': self.url_link,
            'target': 'new',
        }

    def _generate_url_link(self):
        """Generate a unique survey link with both survey and session UUIDs."""
        if not self.url_link:
            survey_uuid = str(uuid.uuid4()) 
            session_uuid = str(uuid.uuid4())  
            self.url_link = f"/survey/{survey_uuid}/{session_uuid}"

    def get_questions(self):
        """Mengambil soal dan pilihan jawaban dari survey."""
        self.ensure_one()
        questions = self.env['survey.question'].search([('survey_id', '=', self.id)])
        
        question_data = []
        for question in questions:
            choices = []
            if question.question_type == 'multiple_choice':
                choices = [{
                    'id': choice.id,
                    'text': choice.value
                } for choice in question.suggested_answer_ids]

            question_data.append({
                'id': question.id,
                'text': question.question,
                'type': question.question_type,
                'choices': choices
            })

        return {
            'survey_id': self.id,
            'questions': question_data
        }

    def submit_answers(self, answers):
        """Menyimpan jawaban pengguna ke `survey.user_input_line`."""
        user_input = self.env['survey.user_input'].create({
            'survey_id': self.id,
            'state': 'done'  
        })

        for answer in answers:
            question = self.env['survey.question'].browse(answer['question_id'])
            if question:
                self.env['survey.user_input_line'].create({
                    'user_input_id': user_input.id,
                    'question_id': question.id,
                    'answer_type': question.question_type,
                    'value_char_box': answer.get('text_answer', ''),
                    'value_suggested_id': answer.get('choice_id', False)
                })

        return {'status': 'success', 'message': 'Answers submitted successfully'}

    @api.model
    def get_questions_from_exam(self, survey_id):
        """Mengambil soal berdasarkan survey_id yang diberikan."""
        survey = self.env['survey.survey'].browse(survey_id)

        if not survey:
            raise ValidationError(_("Survey dengan ID %s tidak ditemukan." % survey_id))
        questions = self.env['survey.question'].search([('survey_id', '=', survey.id)])

        question_data = []

        for question in questions:
            choices = []

            if question.question_type in ['multiple_choice', 'simple_choice']:
                choices = [{
                    'id': choice.id,
                    'text': choice.value
                } for choice in question.suggested_answer_ids]

            question_data.append({
                'id': question.id,
                'text': question.title,  
                'type': question.question_type,
                'choices': choices
            })

        return {
            'survey_id': survey.id,
            'questions': question_data
        }


class SurveyUserInput(models.Model):
    _inherit = "survey.user_input"  

    access_token = fields.Char("Access Token", required=True, default=lambda self: uuid.uuid4().hex)
    scoring_success = fields.Boolean("Scoring Success", default=False)
    start_datetime = fields.Datetime("Start Time", default=fields.Datetime.now)
    end_datetime = fields.Datetime("End Time")
    deadline = fields.Datetime("Deadline")
    scoring_percentage = fields.Float("Scoring Percentage", default=0)
    scoring_total = fields.Float("Scoring Total", default=0)


    @api.model
    def create_survey_user_input(self, survey_id, uid, email=None, nickname=None, deadline=None):
        """ 
        Membuat entri baru di survey.user_input dengan survey_id dan uid sebagai create_uid,
        serta beberapa informasi tambahan.
        """
        survey = self.env['survey.survey'].browse(survey_id)
        if not survey:
            raise ValidationError("Survey tidak ditemukan.")

        user = self.env['res.users'].browse(uid)
        if not user:
            raise ValidationError("User tidak ditemukan.")



        # 🚀 **Override Secara Manual Create UID** 🚀
        user_input = super(self.__class__, self.sudo()).create({
            'survey_id': survey_id,
           
            'state': 'new',
            'access_token': uuid.uuid4().hex,
            'email': email or user.email,
            'nickname': nickname or user.name,
            'test_entry': False,
            'scoring_success': False,
            'start_datetime': fields.Datetime.now(),
            'end_datetime': False,
            'deadline': deadline,
            'scoring_percentage': 0,
            'scoring_total': 0
        })

        # 🔥 **Force Update Create UID dan Write UID Menggunakan Direct SQL** 🔥
        query = """
            UPDATE survey_user_input
            SET create_uid = %s, write_uid = %s
            WHERE id = %s;
        """
        self.env.cr.execute(query, (uid, uid, user_input.id))
        self.env.cr.commit()  # Pastikan perubahan di-commit

        return user_input.id



class SurveyUserInputLine(models.Model):
    _inherit = "survey.user_input.line"

    answer_is_correct = fields.Boolean(string="Correct Answer", default=False)
    answer_score = fields.Float(string="Answer Score", default=0)

    @api.model
    def create(self, vals):
        """ Override create method untuk menentukan score berdasarkan jenis pertanyaan """
        question = self.env["survey.question"].browse(vals.get("question_id"))
        suggested_answer = self.env["survey.question.answer"].browse(vals.get("sugest_answers_id"))

        if question.question_type in ["simple_choice", "multiple_choice"]:
            vals["answer_score"] = suggested_answer.answer_score
            vals["answer_is_correct"] = suggested_answer.is_correct  
        elif question.question_type == "suggestion":
            vals["value_char_box"] = False
            vals["answer_score"] = 0 
            vals["answer_is_correct"] = False  
        elif question.question_type == "char_box":
            vals["suggested_answer_id"] = False
            vals["answer_score"] = 0  
            vals["answer_is_correct"] = False  
        elif question.question_type == "text_box":
            vals["suggested_answer_id"] = False
            vals["answer_score"] = 0  
            vals["answer_is_correct"] = False  

        return super(SurveyUserInputLine, self).create(vals)


    @api.model
    def create_user_input(self, user_input_id, survey_id, question_id, questions_squence, 
                        suggested_answer_id, create_uid, answer_type, value_char_box, value_text_box,
                        answer_score):
        """ Method untuk menerima input dari user dengan args yang telah ditentukan """
        vals = {
            "user_input_id": user_input_id,
            "survey_id": survey_id,
            "question_id": question_id,
            "question_sequence": questions_squence,
            "suggested_answer_id": suggested_answer_id,  # Perbaikan disini
            "create_uid": create_uid,
            "answer_type": answer_type,
            "value_char_box": value_char_box,
            "value_text_box": value_text_box,
            "answer_score": answer_score,
        }
        return self.create(vals)


    @api.model
    def finish_survey(self, survey_id, user_input_id, create_uid):

        # Cari User Input berdasarkan survey_id, user_input_id, dan create_uid
        user_input = self.env['survey.user_input'].search([
            ('survey_id', '=', survey_id),
            ('id', '=', user_input_id),
            ('create_uid', '=', create_uid)
        ], limit=1)

        if not user_input:
            raise ValidationError("Survey User Input tidak ditemukan dengan ID yang diberikan.")

        # Hitung Skor dan Persentase
        total_score = 0
        total_max_score = 0
        for line in user_input.user_input_line_ids:
            total_score += line.answer_score
            total_max_score += line.question_id.suggested_answer_ids.filtered(lambda r: r.is_correct).answer_score

        scoring_percentage = (total_score / total_max_score * 100) if total_max_score else 0

        # Update State User Input
        user_input.write({
            'scoring_percentage': scoring_percentage,
            'scoring_total': total_score,
            'state': 'done', 
            'is_session_answer': False, 
            'end_datetime': fields.Datetime.now(),  
        })

        # Cari Survey
        survey = self.env['survey.survey'].browse(survey_id)
        if not survey:
            raise ValidationError("Survey tidak ditemukan.")

        message = "Selamat! Anda telah berhasil menyelesaikan survey ini."
        result = {}

        if survey.scoring_type == 'no_scoring':
            result = {
                'description': survey.description,
                'scoring_type': survey.scoring_type,
                'answers': [(line.question_id.question_text, line.value_char_box) for line in user_input.user_input_line_ids]
            }
        else:
            result = {
                'description': survey.description,
                'scoring_type': survey.scoring_type,
                'scoring_percentage': scoring_percentage,
                'scoring_total': total_score,
                'answers': [(line.question_id.title, line.value_char_box, line.answer_score) for line in user_input.user_input_line_ids]
            }

        # ** Tambahan: Update Student User Exam berdasarkan survey_id dan student_id **
        student_user_exam = self.env['student_user_exam'].search([
            ('survey_id', '=', survey_id),
            ('student_id', '=', create_uid)  # Pastikan field ini sesuai dengan model yang digunakan
        ], limit=1)

        if student_user_exam:
            student_user_exam.sudo().write({
                'is_fill': True
            })
        else:
            raise ValidationError("Student User Exam tidak ditemukan untuk survey dan student ini.")

        return {'message': message, 'result': result}



class SurveyQuestion(models.Model):
    _inherit = 'survey.question'  
    
    max_score = fields.Integer('Max Score')