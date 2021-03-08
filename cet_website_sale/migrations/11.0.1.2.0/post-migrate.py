# Copyright 2020 Coop IT Easy SCRLfs <http://coopiteasy.be>
#   Rémy Taymans <remy@coopiteasy.be>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


def migrate(cr, version):
    # Get old categ
    cr.execute(
        """
        SELECT id, name, website_restrict_product, active
        FROM backup_res_partner_customer_type
        """
    )
    categs = cr.fetchall()
    # Fill new customer type and relation with products
    for categ in categs:
        # Get products of the current categ
        cr.execute(
            """
            SELECT product_product_id
            FROM backup_product_product_res_partner_category_rel
            WHERE res_partner_category_id = %s
            """,
            (categ[0],),
        )
        products = cr.fetchall()
        # Create new customer type and get back its id
        cr.execute(
            """
            INSERT INTO res_partner_customer_type (
                name,
                website_restrict_product,
                active
            ) VALUES (%s, %s, %s)
            RETURNING id
            """,
            (categ[1], categ[2], categ[3]),
        )
        customer_type_id = cr.fetchone()[0]
        # Link product to the new customer type
        type_product_rel_vals = (
            (customer_type_id, product[0]) for product in products
        )
        cr.executemany(
            """
            INSERT INTO product_product_res_partner_customer_type_rel (
                res_partner_customer_type_id,
                product_product_id
            ) VALUES (%s, %s)
            """,
            type_product_rel_vals,
        )
        # Get all partner assigned to this categ
        cr.execute(
            """
            SELECT partner_id FROM res_partner_res_partner_category_rel
            WHERE category_id = %s
            """,
            (categ[0],),
        )
        partners = cr.fetchall()
        partner_customer_type_vals = (
            (customer_type_id, partner[0]) for partner in partners
        )
        cr.executemany(
            "UPDATE res_partner SET customer_type_id = %s WHERE id = %s",
            partner_customer_type_vals,
        )

    # Delete backup tables
    cr.execute(
        """
        DROP TABLE backup_product_product_res_partner_category_rel
        """
    )
    cr.execute(
        """
        DROP TABLE backup_res_partner_customer_type
        """
    )
