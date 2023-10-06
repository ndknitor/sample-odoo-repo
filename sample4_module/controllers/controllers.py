# -*- coding: utf-8 -*-
# from odoo import http


# class Sample4Module(http.Controller):
#     @http.route('/sample4_module/sample4_module', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/sample4_module/sample4_module/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('sample4_module.listing', {
#             'root': '/sample4_module/sample4_module',
#             'objects': http.request.env['sample4_module.sample4_module'].search([]),
#         })

#     @http.route('/sample4_module/sample4_module/objects/<model("sample4_module.sample4_module"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('sample4_module.object', {
#             'object': obj
#         })
