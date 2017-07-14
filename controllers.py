# -*- coding: utf-8 -*-
from openerp import http

# class AssetsManage(http.Controller):
#     @http.route('/assets_manage/assets_manage/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/assets_manage/assets_manage/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('assets_manage.listing', {
#             'root': '/assets_manage/assets_manage',
#             'objects': http.request.env['assets_manage.assets_manage'].search([]),
#         })

#     @http.route('/assets_manage/assets_manage/objects/<model("assets_manage.assets_manage"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('assets_manage.object', {
#             'object': obj
#         })