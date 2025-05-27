from odoo import models, fields, api

class NewsType(models.Model):
    _name = 'news.type'
    _description = 'News Type'
    _rec_name = 'jenis'

    jenis = fields.Char(string='Type', required=True)
    description = fields.Text(string='Description')

class OpNews(models.Model):
    _name = 'op.news'
    _description = 'OpenEduCat News'
    _order = 'dipublikasikan_pada desc'

    sumber = fields.Char(string='Source', required=True)
    author = fields.Char(string='Author', required=True)
    judul = fields.Char(string='Title', required=True)
    keterangan = fields.Text(string='Description', required=True)
    
    gambar1 = fields.Binary(string='Image 1', attachment=True)
    gambar2 = fields.Binary(string='Image 2', attachment=True)
    gambar3 = fields.Binary(string='Image 3', attachment=True)
    gambar4 = fields.Binary(string='Image 4', attachment=True)
    gambar5 = fields.Binary(string='Image 5', attachment=True)
    
    dipublikasikan_pada = fields.Datetime(string='Published On', default=fields.Datetime.now)
    isi = fields.Html(string='Content')
    
    id_jenis = fields.Many2one('news.type', string='News Type', required=True)
