odoo.define('cet_website_sale', function (require) {
    'use strict';

    require('web.dom_ready');
    var ajax = require('web.ajax');


    if (!$('.oe_website_sale').length) {
        return $.Deferred().reject("DOM doesn't contain '.oe_website_sale'");
    }

    function check_stock () {

        /**
         * This function gets information about stock for a product
         * variant and it disables action button when needed. It also
         * shows messages about the stock when appropriated.
         */

        // The variable 'this' must contain an input with value equal
        // to the product variant id.
        var input = this;

        ajax.jsonRpc("/shop/product/stock_info",
            'call',
            {'id': parseInt($(input).attr("value"), 10)})
            .then(function (stock_info) {
                // Select element on the page
                var js_product = $(input).closest('.js_product');
                var qty_input = $(js_product).find('input[name="add_qty"]');
                var qty = qty_input.val();

                // Check only if the inventory_availability is 'always' or
                // 'threshold'
                if (stock_info.inventory_availability === 'always' ||
                    stock_info.inventory_availability === 'threshold') {

                    // If there is a threshold, remove it from the
                    // available quantity
                    if (stock_info.inventory_availability === 'threshold') {
                        stock_info.virtual_available -=
                            stock_info.available_threshold;
                    }

                    // Remove quantity in a cart from the available quantity
                    stock_info.virtual_available -=
                        parseInt(stock_info.cart_qty, 10);

                    // Set quantity to 0 in case of a negative value after
                    // computations
                    if (stock_info.virtual_available < 0) {
                        stock_info.virtual_available = 0;
                    }

                    // Prevent qty to grow above the available quantity
                    if (qty > stock_info.virtual_available) {
                        qty = stock_info.virtual_available || 1;
                        qty_input.val(qty);
                    }

                    // Disable button "Add to cart"
                    var disable_condition =
                        qty > stock_info.virtual_available ||
                        stock_info.virtual_available < 1 ||
                        qty < 1
                    ;
                    $(js_product).find('#add_to_cart').toggleClass(
                        'disabled',
                        disable_condition
                    );

                    // Disable 'add quantity' button when reaching maximum
                    // available quantity.
                    $(js_product).find('.js_add').toggleClass(
                        'disabled btn',
                        stock_info.virtual_available - qty < 1
                    );
                    $(js_product).find('.js_remove').toggleClass(
                        'disabled btn',
                        qty <= 1
                    );

                    // Display message
                    $(js_product).find('.oe_stock_messages').toggleClass(
                        'hidden',
                        stock_info.virtual_available - qty >= 1
                    );
                }

            });
    }

    $('.oe_website_sale').each(function () {
        var oe_website_sale = this;

        // At page load, run check_stock() on each input containing a product_id
        $(oe_website_sale).find('input[name="product_id"]').each(check_stock);

        // Run check_stock() when changing status of an input
        $(oe_website_sale).find('input[name="product_id"]')
            .on('change', check_stock);

        // Run check_stock() when input quantity status changed
        $(oe_website_sale).find('input[name=qty]').on('change', check_stock);
    });

});
