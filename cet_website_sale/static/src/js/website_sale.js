odoo.define('cet_website_sale.website_sale', function (require) {
    "use strict";

    require('web.dom_ready');

    $('.oe_website_sale').each(function () {
        var oe_website_sale = this;

        $(oe_website_sale).on('change', '.js_product_change_select', function () {
            var product_id = $(this).val();
            var $cet_product_variant = $(this).closest('.oe_cet_product_variant');
            var $input = $cet_product_variant.find('input[vid="'+product_id+'"]');
            $input.prop( "checked", true ).change();
        });
    });
});
