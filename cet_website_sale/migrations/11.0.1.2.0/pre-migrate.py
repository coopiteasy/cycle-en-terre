# Copyright 2020 Coop IT Easy SCRLfs <http://coopiteasy.be>
#   Rémy Taymans <remy@coopiteasy.be>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


def migrate(cr, version):
    # Backup relation between tags and products
    cr.execute(
        """
        CREATE TABLE IF NOT EXISTS backup_product_product_res_partner_category_rel
        AS TABLE product_product_res_partner_category_rel
        """
    )

    # Keep old tags that appears in the previous table
    cr.execute(
        """
        CREATE TABLE IF NOT EXISTS backup_res_partner_customer_type
        AS SELECT id, name, website_restrict_product, active
        FROM res_partner_category
        WHERE id in (
            SELECT DISTINCT res_partner_category_id
            FROM product_product_res_partner_category_rel
        )
        """
    )
