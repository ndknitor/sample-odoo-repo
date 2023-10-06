# -*- coding: utf-8 -*-
# from odoo import http


# class Sample5Module(http.Controller):
#     @http.route('/sample5_module/sample5_module', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/sample5_module/sample5_module/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('sample5_module.listing', {
#             'root': '/sample5_module/sample5_module',
#             'objects': http.request.env['sample5_module.sample5_module'].search([]),
#         })

#     @http.route('/sample5_module/sample5_module/objects/<model("sample5_module.sample5_module"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('sample5_module.object', {
#             'object': obj
#         })
