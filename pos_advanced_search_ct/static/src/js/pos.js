odoo.define('pos_advanced_search_ct.pos', function (require) {
	"use strict";

	var screens = require('point_of_sale.screens');

	screens.ProductCategoriesWidget.include({
        renderElement: function(){
            this._super();
            var self = this;
            $(".searchbox input").autocomplete({
                source: function (request, response) {
//                    response([{ label: 'Example', value: 'ex'  }]);
                    response(self.get_product_list(self.category,request.term));
                },
                select: function(event, ui){
                    var product = self.pos.db.get_product_by_id(ui.item['id']);
                    self.clear_search();
                    self.pos.get_order().add_product(product);
                    return false;
                },
            });
        },
        get_product_list: function(category,query){
            var product_list = []
            var products;
            if(query){
                products = this.pos.db.search_product_in_category(category.id,query);
            }else{
                products = this.pos.db.get_product_by_category(this.category.id);
            }
            products.map(function(product){
                var values = {
                    'id': product.id,
                    'values': product.display_name,
                }
                if(product.default_code){
                    values['label'] = "["+product.default_code+"] "+product.display_name;
                }else{
                    values['label'] = product.display_name;
                }
                product_list.push(values);
            });
            return product_list;
        }
    });

});