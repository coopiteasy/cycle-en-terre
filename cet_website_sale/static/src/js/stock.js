odoo.define('cet_website_sale', function(require) {
'use strict';

require('web.dom_ready');
var base = require('web_editor.base');
var ajax = require('web.ajax');
var core = require('web.core');

var QWeb = core.qweb;
var xml_load = ajax.loadXML('/cet_website_sale/static/src/xml/stock_messages.xml', QWeb);

if(!$('.oe_website_sale').length) {
  return $.Deferred().reject("DOM doesn't contain '.oe_website_sale'");
}

$('.oe_website_sale').each(function() {
  var oe_website_sale = this;

  $(oe_website_sale).find('#oe_variant_ids_selector input')
    .on('change', function(event) {
      var input = this;

      ajax.jsonRpc("/shop/product/stock_info",
        'call',
        {'id': parseInt($(input).attr("value"))})
        .then(function(stock_info){
          // Select element on the page
          var js_product = $(input).closest('.js_product');
          var qty_input = $(js_product).find('input[name="add_qty"]');
          var qty = qty_input.val();

          // Check only if the inventory_availability is 'always' or
          // 'threshold'
          if (stock_info['inventory_availability'] === 'always'
              || stock_info['inventory_availability'] === 'threshold') {

            // If there is a threshold, remove it from the available quantity
            if (stock_info['inventory_availability'] === 'threshold') {
              stock_info['virtual_available'] -= stock_info['available_threshold'];
            }

            // Remove quantity in a cart from the available quantity
            stock_info['virtual_available'] -= parseInt(stock_info['cart_qty']);

            // Set quantity to 0 in case of a negative value after
            // computations
            if (stock_info['virtual_available'] < 0) {
              stock_info['virtual_available'] = 0;
            }

            // Prevent qty to grow above the available quantity
            if (qty > stock_info['virtual_available']) {
              qty = stock_info['virtual_available'] || 1;
              qty_input.val(qty);
            }

            // Disable button "Add to cart"
            var disable_condition = (
              qty > stock_info['virtual_available']
              || stock_info['virtual_available'] < 1
              || qty < 1
            );
            $(js_product).find('#add_to_cart').toggleClass(
              'disabled',
              disable_condition
            );

            // Disable 'add quantity' button when reaching maximum
            // available quantity.
            $(js_product).find('.js_add').toggleClass(
              'disabled btn',
              stock_info['virtual_available'] - qty < 1
            );
            $(js_product).find('.js_remove').toggleClass(
              'disabled btn',
              qty <= 1
            );

            // Display message
            $(js_product).find('.oe_stock_messages').toggleClass(
              'hidden',
              stock_info['virtual_available'] - qty >= 1
            );
          }

          xml_load.then(function() {
            var message = $(QWeb.render('cet_website_sale.stock_messages', stock_info));
            $(js_product).find('.oe_stock_messages').html(message);
          });

        });
    });

});

});
