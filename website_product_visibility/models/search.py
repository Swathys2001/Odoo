# -*- coding: utf-8 -*-
from odoo import models
from odoo.http import request


class WebsiteSearchFetching(models.AbstractModel):
    """used to override search function with require products"""
    _inherit = 'website.searchable.mixin'

    def _search_fetch(self, search_detail, search, limit, order):
        """override search function with require products"""
        super()._search_fetch(search_detail, search, limit, order)
        products = request.env.user.partner_id.allowed_product_ids
        category = request.env.user.partner_id.allowed_product_category_ids
        fields = search_detail['search_fields']
        base_domain = search_detail['base_domain']
        domain = self._search_build_domain(base_domain, search, fields,
                                           search_detail.get('search_extra'))
        model = self.sudo() if search_detail.get('requires_sudo') else self
        results = model.search(
            domain,
            limit=limit,
            order=search_detail.get('order', order)
        )
        results = results.browse(products.ids) + results.browse(category.ids)
        count = model.search_count(domain)
        return results, count
