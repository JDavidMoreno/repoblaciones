# -*- coding: utf-8 -*-
from odoo import http

# class Repoblaciones(http.Controller):
#     @http.route('/repoblaciones/repoblaciones/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/repoblaciones/repoblaciones/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('repoblaciones.listing', {
#             'root': '/repoblaciones/repoblaciones',
#             'objects': http.request.env['repoblaciones.repoblaciones'].search([]),
#         })

#     @http.route('/repoblaciones/repoblaciones/objects/<model("repoblaciones.repoblaciones"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('repoblaciones.object', {
#             'object': obj
#         })