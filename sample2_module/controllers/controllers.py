# -*- coding: utf-8 -*-
# from odoo import http


# class Sample2Module(http.Controller):
#     @http.route('/sample2_module/sample2_module', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/sample2_module/sample2_module/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('sample2_module.listing', {
#             'root': '/sample2_module/sample2_module',
#             'objects': http.request.env['sample2_module.sample2_module'].search([]),
#         })

#     @http.route('/sample2_module/sample2_module/objects/<model("sample2_module.sample2_module"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('sample2_module.object', {
#             'object': obj
#         })
