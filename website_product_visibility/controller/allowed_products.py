# -*- coding: utf-8 -*-
"""website sale shop"""
from odoo.addons.website_sale.controllers.main import WebsiteSale, TableCompute
from odoo import http
from odoo.http import request
from odoo.tools import lazy


class WebsiteSaleInherit(WebsiteSale):
    """Inherited class of website sale"""

    @http.route()
    def shop(self, page=0, category=None, search='', ppg=False, **post):
        """override website shop to restrict product visibility to users"""
        shop_super = super(WebsiteSaleInherit, self).shop(
            page=page, category=category, search=search, ppg=ppg, **post)
        user = request.env.user
        users_category = user.partner_id.allowed_product_category_ids
        category_product = request.env['product.template'].sudo().search(
            [('public_categ_ids', 'in', [cat.id for cat in users_category])])
        products = user.partner_id.allowed_product_ids + category_product
        if user.partner_id.allowed_product_ids:
            price_list = request.env['product.pricelist'].browse(
                request.session.get('website_sale_current_pl'))
            products_prices = (
                lazy(lambda: products._get_sales_prices(price_list)))
            attributes = lazy(lambda: request.env['product.attribute'].search([
                ('product_tmpl_ids', 'in', products.ids),
            ]))
            website = request.env['website'].get_current_website()
            url = "/shop/"
            if category:
                url = "/shop/category"
            product_per_page = shop_super.qcontext.get('ppg')
            pager = website.pager(url=url, total=len(products), page=page,
                                  step=product_per_page, scope=7, url_args=post)
            ppr = website.shop_ppr or 1
            bins = lazy(lambda: TableCompute().process(products, ppg, ppr))
            shop_super.qcontext.update({
                'pager': pager,
                'pricelist': price_list,
                'products': products, 'bins': bins,
                'categories': users_category,
                'attributes': attributes,
                'search_product': products,
                'search_categories_ids': users_category,
                'get_product_prices': lambda pro:
                lazy(lambda: products_prices[pro.id]),
            })
            if category:
                product = request.env['product.template'].sudo().search(
                    [('public_categ_ids', 'in', [cat.id for cat in category])])
                shop_super.qcontext.update({
                    'category': category,
                    'products': product,
                    'bins': lazy(
                         lambda: TableCompute().process(
                             product, ppg, ppr))
                    })
            return shop_super
