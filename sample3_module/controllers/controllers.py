# -*- coding: utf-8 -*-
# from odoo import http


# class Sample3Module(http.Controller):
#     @http.route('/sample3_module/sample3_module', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/sample3_module/sample3_module/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('sample3_module.listing', {
#             'root': '/sample3_module/sample3_module',
#             'objects': http.request.env['sample3_module.sample3_module'].search([]),
#         })

#     @http.route('/sample3_module/sample3_module/objects/<model("sample3_module.sample3_module"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('sample3_module.object', {
#             'object': obj
#         })
