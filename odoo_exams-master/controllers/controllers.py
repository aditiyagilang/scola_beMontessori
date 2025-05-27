import json
import logging
import werkzeug
import werkzeug.utils
from datetime import datetime
from math import ceil

from odoo import SUPERUSER_ID

from odoo import http
from odoo.http import request
from odoo.tools.misc import DEFAULT_SERVER_DATETIME_FORMAT as DTF, ustr

_logger = logging.getLogger(__name__)

class WebsiteSurvey(http.Controller):

    @http.route(['/survey/scores/<model("survey.survey"):survey>/<string:token>'],
                type='http', auth='public', website=True)
    def get_scores(self, survey, token, page=None, **post):
        cr, uid, context = request.cr, request.uid, request.context
        user_input_line_obj = request.registry['survey.user_input_line']
        ret = {}

        # Fetch answers
        ids = user_input_line_obj.search(cr, SUPERUSER_ID, [('user_input_id.token', '=', token)], context=context)
        previous_answers = user_input_line_obj.browse(cr, uid, ids, context=context)

        # Compute score for each question
        for answer in previous_answers:
            tmp_score = ret.get(answer.question_id.id, 0.0)
            ret.update({answer.question_id.id: tmp_score + answer.quizz_mark})
            if json.dumps(ret)<70:
                return "Fail"
            elif json.dumps(ret)>=70:
               return "Pass"

    # AJAX submission of a page
    @http.route(['/survey/submit/<model("survey.survey"):survey>'],
                type='http', methods=['POST'], auth='public', website=True, csrf=False)
    def submit(self, survey, **post):
        _logger.debug('Incoming data: %s', post)
        print(post)
        page_id = int(post['page_id'])
        cr, uid, context = request.cr, request.uid, request.context
        survey_obj = request.registry['survey.survey']
        questions_obj = request.registry['survey.question']
        questions_ids = questions_obj.search(cr, uid, [('page_id', '=', page_id)], context=context)
        questions = questions_obj.browse(cr, uid, questions_ids, context=context)

        # Answer validation
        errors = {}
        for question in questions:
            answer_tag = "%s_%s_%s" % (survey.id, page_id, question.id)
            errors.update(questions_obj.validate_question(cr, uid, question, post, answer_tag, context=context))

        ret = {}
        if (len(errors) != 0):
            # Return errors messages to webpage
            ret['errors'] = errors
        else:
            # Store answers into database
            user_input_obj = request.registry['survey.user_input']

            user_input_line_obj = request.registry['survey.user_input_line']
            try:
                user_input_id = user_input_obj.search(cr, SUPERUSER_ID, [('token', '=', post['token'])], context=context)[0]
            except KeyError:  # Invalid token
                return request.website.render("website.403")
            user_input = user_input_obj.browse(cr, SUPERUSER_ID, user_input_id, context=context)
            user_id = uid if user_input.type != 'link' else SUPERUSER_ID
            for question in questions:
                answer_tag = "%s_%s_%s" % (survey.id, page_id, question.id)
                user_input_line_obj.save_lines(cr, user_id, user_input_id, question, post, answer_tag, context=context)

            go_back = post['button_submit'] == 'previous'
            next_page, _, last = survey_obj.next_page(cr, uid, user_input, page_id, go_back=go_back, context=context)
            vals = {'last_displayed_page_id': page_id}
            if next_page is None and not go_back:
                vals.update({'state': 'done'})
            else:
                vals.update({'state': 'skip'})
            user_input_obj.write(cr, user_id, user_input_id, vals, context=context)
            ret['redirect'] = '/survey/fill/%s/%s' % (survey.id, post['token'])
            if go_back:
                ret['redirect'] += '/prev'
        return json.dumps(ret)

#
# # class Examination(http.Controller):
# #     @http.route('/examination/examination/', auth='public')
# #     def index(self, **kw):
# #         return "Hello, world"
#
# #     @http.route('/examination/examination/objects/', auth='public')
# #     def list(self, **kw):
# #         return http.request.render('examination.listing', {
# #             'root': '/examination/examination',
# #             'objects': http.request.env['examination.examination'].search([]),
# #         })
#
# #     @http.route('/examination/examination/objects/<model("examination.examination"):obj>/', auth='public')
# #     def object(self, obj, **kw):
# #         return http.request.render('examination.object', {
# #             'object': obj
# #         })
