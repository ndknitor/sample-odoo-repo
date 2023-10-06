# -*- coding: utf-8 -*-
# from odoo import http


# class Sample1Module(http.Controller):
#     @http.route('/sample1_module/sample1_module', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/sample1_module/sample1_module/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('sample1_module.listing', {
#             'root': '/sample1_module/sample1_module',
#             'objects': http.request.env['sample1_module.sample1_module'].search([]),
#         })

#     @http.route('/sample1_module/sample1_module/objects/<model("sample1_module.sample1_module"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('sample1_module.object', {
#             'object': obj
#         })
