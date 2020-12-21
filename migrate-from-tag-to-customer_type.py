# This script is based on the state of the CeT database on the 2020-12-21
#
# This script should be run after upgrading the CeT database.
# The script does the following:
#   - Rename Customer Type
#   - Assign Customer Type to partner based on the partner tags.
#
# Run this script with:
# cat migrate-from-tag-to-customer_type.py | odoo shell -c odoo.conf -d dbname

import sys

# This line is a hack to easy conversion to click-odoo
env = self.env


# Get customer type
revendeur = env["res.partner.customer.type"].search(
    ["|", ("name", "ilike", "accès revendeur"), ("name", "=", "Revendeur")]
)
if not revendeur:
    print("Error: 'accès revendeur' customer type not found.", file=sys.stderr)
    sys.exit(1)
else:
    # Rename
    revendeur.name = "Revendeur"

maraicher = env["res.partner.customer.type"].search(
    [("name", "ilike", "maraicher")]
)
if not maraicher:
    maraicher = env["res.partner.customer.type"].create(
        {
            "name": "Maraicher",
            "show_on_website": False,
        }
    )

particulier = env["res.partner.customer.type"].search(
    [("name", "ilike", "particulier")]
)
if not particulier:
    particulier = env["res.partner.customer.type"].create(
        {
            "name": "Particulier",
            "show_on_website": False,
        }
    )

# Get tags
tag_revendeur = env["res.partner.category"].search(
    [("name", "ilike", "revendeur actif")]
)
if not tag_revendeur:
    print("Error: 'revendeur actif' tag not found.", file=sys.stderr)
    sys.exit(1)

tag_maraicher = env["res.partner.category"].search(
    [("name", "ilike", "Maraîcher/Agriculteur")]
)
if not tag_maraicher:
    print("Error: 'Maraîcher/Agriculteur' tag not found.", file=sys.stderr)
    sys.exit(1)

# Set right customer type
partners = env["res.partner"].search([])
for partner in partners:
    commercial_partner_id = partner.commercial_partner_id
    print("Debug: {}: {}, {}: {}".format(
        partner.id,
        partner.name,
        commercial_partner_id.name,
        ", ".join([cat.name for cat in commercial_partner_id.category_id])
    ))
    if tag_revendeur in commercial_partner_id.category_id:
        commercial_partner_id.customer_type_id = revendeur
        print("Info: Assign {} to {}:{}".format(
            revendeur.name,
            commercial_partner_id.id,
            commercial_partner_id.name
        ))
    elif tag_maraicher in commercial_partner_id.category_id:
        commercial_partner_id.customer_type_id = maraicher
        print("Info: Assign {} to {}:{}".format(
            maraicher.name,
            commercial_partner_id.id,
            commercial_partner_id.name
        ))
    elif commercial_partner_id:
        commercial_partner_id.customer_type_id = particulier
        print("Info: Assign {} to {}:{}".format(
            particulier.name,
            commercial_partner_id.id,
            commercial_partner_id.name
        ))

# Commit only if run with odoo shell. Do not commit if running with
# click-odoo
env.cr.commit()
